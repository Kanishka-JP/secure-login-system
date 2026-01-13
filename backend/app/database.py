import firebase_admin
from firebase_admin import credentials, firestore
import os, json

cred_json = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)
db = firestore.client()

