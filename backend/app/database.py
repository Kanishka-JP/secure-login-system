import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Prevent double initialization
if not firebase_admin._apps:
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS_JSON")

    if not firebase_credentials:
        raise RuntimeError("FIREBASE_CREDENTIALS_JSON not set")

    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
