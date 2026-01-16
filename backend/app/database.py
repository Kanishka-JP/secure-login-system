import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

if not cred_json:
    raise RuntimeError("FIREBASE_CREDENTIALS_JSON not set")

cred = credentials.Certificate(json.loads(cred_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
