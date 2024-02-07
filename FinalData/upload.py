from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential
import sys

# Connect to the AzureML workspace
subscription_id = '19f75306-19b2-450f-a135-9045333bbb48'
resource_group = 'babel'
workspace = 'babel-oai-south-central-us'

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# Set the version number of the data asset (for example: '1')
VERSION = "1"

# Set the path, supported paths include:
# local: './<path>/<folder>' (this will be automatically uploaded to cloud storage)
# blob:  'wasbs://<container_name>@<account_name>.blob.core.windows.net/<path>/<folder>'
# ADLS gen2: 'abfss://<file_system>@<account_name>.dfs.core.windows.net/<path>/<folder>'
# Datastore: 'azureml://datastores/<data_store_name>/paths/<path>/<folder>'
path = sys.argv[1]

# Define the Data asset object
my_data = Data(
    path=path,
    type=AssetTypes.URI_FOLDER,
    description="",
    name="test_upload_data_from_cli_2",
    version=VERSION,
)

# Create the data asset in the workspace
ml_client.data.create_or_update(my_data)
