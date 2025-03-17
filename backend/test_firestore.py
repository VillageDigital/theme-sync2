from dotenv import load_dotenv
load_dotenv()

import os
from google.cloud import firestore

# Confirm environment variable is loaded
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print("Credentials loaded from:", credentials_path)

# Initialize Firestore client
db = firestore.Client()

# Reference to a collection
collection_ref = db.collection('themes')

# Add data to Firestore (storing a new document)
def add_data_to_firestore(doc_id, data):
    doc_ref = collection_ref.document(doc_id)
    doc_ref.set(data)
    print(f"Document added with ID: {doc_id}")

# Example data to store
data = {
    "name": "Sample Theme",
    "version": "1.0.0",
    "last_updated": firestore.SERVER_TIMESTAMP
}

# Call function to add data
add_data_to_firestore("theme_1", data)
