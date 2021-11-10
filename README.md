# azure-sub-sync

An Azure Function for syncing subscriptions with your Canonical private offer.

## Setup

1.  Start by informing your Canonical account manager that you want to start
    managing your private offer through the azure-sub-sync workflow.

2.  For each Azure Subscription that you want to grant access to the private
    offer, [tag the subscription](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json) with
    the tag name `ubuntu-pro` and value `1`. (See "Tagging" below.)

3.  Create a private fork of this repository on GitHub, and connect it to an
    Azure Function App (Python runtime) following
    [these instructions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions?tabs=dotnet).

4.  On the storage account you selected while setting up your Azure Function
    App, create an ``ubuntuprosubscriptions`` storage table.

5.  Ensure the function runs at least once. You can use the
    [Azure Storage Explorer](https://docs.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer?tabs=linux) to confirm
    that the storage table is populated with subscription IDs.

6.  [[TO DO: How do they share the table with us?]]

## Tagging

By default, `azure-sub-sync` will pick up all subscriptions tagged with the
key-value pair `ubuntu-pro:1`. You can change the expected key or value by
modifying the constants `SUB_TAG_KEY` and `SUB_TAG_VAL` at the top of
`azure-sub-sync/__init__.py`.

If `SUB_TAG_KEY` is an empty string, *all* subscriptions on the tenant will be
collected. In this case, `SUB_TAG_VAL` is ignored.

## Removing Subscriptions

Untagging or deleting a subscription will *NOT* remove it from the storage
table. Instead, you will need to manually remove the entries with
[Azure Storage Explorer](https://docs.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer?tabs=linux).

If you need to remove many subscriptions at once, you can also delete and
recreate the storage table. However, if you plan to do this,
**please contact Canonical to coordinate**. This is necessary since our
scripts automatically update the private offer access permissions from the
storage table; if our scripts pull in an empty table, it could take a few
business days to update the private offer again.
