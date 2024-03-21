from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

app = Flask(__name__)

# Azure Storage Account connection string
connection_string = os.getenv('STORAGE_CONNECTION_STRING')
container_name = os.getenv('CONTAINER_NAME')


# Function to connect to Azure Storage Account Blob Container


def connect_to_blob_container():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)
        container_client = blob_service_client.get_container_client(
            container_name)
        return container_client
    except Exception as e:
        print("Error connecting to blob container:", e)
        return None

# API endpoint to upload file to Azure Blob Storage


@app.route('/upload_file', methods=['GET'])
def upload_file():
    try:
        container_client = connect_to_blob_container()
        if container_client:
            # File path to upload
            file_path = "sample.txt"

            # Open the file in binary read mode
            with open(file_path, "rb") as file:
                blob_name = os.path.basename(file_path)
                blob_client = container_client.get_blob_client(blob_name)

                # Upload the file content to the blob
                blob_client.upload_blob(file)

            return jsonify({"message": f"File '{blob_name}' uploaded successfully"}), 200
        else:
            return jsonify({"error": "Failed to connect to blob container"}), 500
    except Exception as e:
        print("Error uploading file:", e)
        return jsonify({"error": "Failed to upload file"}), 500


if __name__ == '__main__':
    app.run(debug=True)
