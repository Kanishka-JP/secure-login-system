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
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")