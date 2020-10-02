from google.cloud import bigquery
from dotenv import load_dotenv
import pprint

load_dotenv()
"""
this file creates a dataset named taxi in your project
"""
def create_dataset():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to create.
    dataset_id = "{}.taxi".format(client.project)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    # TODO(developer): Specify the geographic location where the dataset should reside.
    dataset.location = "US"

    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

if __name__=="__main__":
    create_dataset()