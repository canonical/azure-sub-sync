import json

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient, models
from azure.mgmt.resource import SubscriptionClient


"""The tag key and value that must be present on each included subscription."""
SUB_TAG_KEY = 'ubuntu-pro'
SUB_TAG_VAL = '1'


def get_subscriptions(tag_key=SUB_TAG_KEY, tag_val=SUB_TAG_VAL):
    """Returns a set containing all the subscriptions with the given tag
    key and value. If tag key is empty, all subscriptions will be retrieved.
    """

    cred = DefaultAzureCredential()

    subs = [
        sub.as_dict()['subscription_id']
        for sub in SubscriptionClient(credential=cred).subscriptions.list()
    ]

    tag_query = f"where tags['{tag_key}'] =~ '{tag_val}' | " if tag_key else ""

    query = (
        "ResourceContainers | "
        "where type =~ 'microsoft.resources/subscriptions' | "
        f"{tag_query}"
        "project subscriptionId"
    )

    options = models.QueryRequestOptions(result_format="objectArray")

    # create query
    query_request = models.QueryRequest(
        subscriptions=subs, query=query, options=options
    )

    # run query
    query_client = ResourceGraphClient(cred)

    results = set()
    query_response = query_client.resources(query_request).as_dict()

    for result in query_response['data']:
        for entry in result.values():
            results.add(entry)

    return results


def main(timer: func.TimerRequest, inputTable, outputTable) -> None:
    all_subs = get_subscriptions()

    in_data = json.loads(inputTable)
    stored_subs = {val['RowKey'] for val in in_data}

    add_subs = all_subs.difference(stored_subs)

    write_data = [{"RowKey": x} for x in add_subs]
    outputTable.set(json.dumps(write_data))
