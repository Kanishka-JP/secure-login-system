from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

app = FastAPI(
    title="Secure Login System",
    version="1.0"
)

# ✅ ADD THIS (CORS CONFIG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "https://secure-login-system.vercel.app"  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "Backend running"}
