import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- JWT CONFIG ----------------
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

# ---------------- APP CONFIG ----------------
ISSUER_NAME = os.getenv("ISSUER_NAME", "SecureLogin")

# ---------------- EMAIL CONFIG ----------------
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
