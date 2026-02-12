from fastapi import APIRouter, Depends
from Dependency import get_current_user
from database import get_connection

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/")
def get_profile(user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name,email FROM users WHERE id=%s", (user["id"],))
    profile = cursor.fetchone()

    conn.close()
    return {"name": profile[0], "email": profile[1]}
