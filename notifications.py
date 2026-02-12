from fastapi import APIRouter, Depends
from Dependency import get_current_user
from database import get_connection

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT message FROM notifications WHERE user_id=%s", (user["id"],))
    rows = cursor.fetchall()

    conn.close()
    return {"notifications": [r[0] for r in rows]}
