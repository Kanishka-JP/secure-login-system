import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load .env file
load_dotenv()

firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

if not firebase_json:
    raise RuntimeError("FIREBASE_CREDENTIALS_JSON not set")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
