from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_connection
from config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# ----------------------------
# Models
# ----------------------------

class SignupModel(BaseModel):
    name: str
    email: EmailStr
    password: str


class SigninModel(BaseModel):
    email: EmailStr
    password: str


# ----------------------------
# Helper Functions
# ----------------------------

def create_token(email: str):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def response(success: bool, message: str, data=None, status_code=200):
    return {
        "statusCode": status_code,
        "success": success,
        "message": message,
        "data": data
    }


# ----------------------------
# SIGNUP
# ----------------------------

@router.post("/signup")
def signup(data: SignupModel):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check existing user
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (data.email,))
        if cursor.fetchone():
            return response(False, "Email already registered", None, 400)

        hashed_password = hash_password(data.password)

        cursor.execute("""
            INSERT INTO users (name, email, password, is_verified)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id
        """, (data.name, data.email, hashed_password))

        user_id = cursor.fetchone()[0]
        conn.commit()

        return response(
            True,
            "Signup successful",
            {"user_id": user_id},
            201
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()


# ----------------------------
# SIGNIN
# ----------------------------

@router.post("/signin")
def signin(data: SigninModel):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email, password
            FROM users
            WHERE email = %s
        """, (data.email,))

        user = cursor.fetchone()

        if not user:
            return response(False, "User not found", None, 400)

        user_id, name, email, hashed_password = user

        if not verify_password(data.password, hashed_password):
            return response(False, "Invalid credentials", None, 400)

        token = create_token(email)

        return response(
            True,
            "Signin successful",
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "access_token": token
            },
            200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()
