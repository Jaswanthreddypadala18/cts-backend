from fastapi import APIRouter, Depends
from schemas import CreateGroupSchema
from database import get_connection
from Dependency import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/")
def create_group(data: CreateGroupSchema, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO groups (created_by,group_name) VALUES (%s,%s) RETURNING id",
        (user["id"], data.group_name)
    )
    group_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO group_members (group_id,user_id,role) VALUES (%s,%s,'admin')",
        (group_id, user["id"])
    )

    conn.commit()
    conn.close()

    return {"group_id": group_id}
