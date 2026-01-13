from app.database import db

db.collection("test").document("check").set({
    "status": "firebase connected"
})

print("Firebase connection successful")
