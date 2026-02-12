from fastapi import APIRouter, Depends
from datetime import datetime, date, timedelta
import pytz
from schemas import AvailabilitySchema
from database import get_connection
from Dependency import get_current_user

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.post("/")
def set_availability(data: AvailabilitySchema, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT timezone FROM users WHERE id=%s", (user["id"],))
    tz = pytz.timezone(cursor.fetchone()[0])

    from_time = datetime.strptime(data.from_time, "%H:%M").time()
    to_time = datetime.strptime(data.to_time, "%H:%M").time()

    local_from = tz.localize(datetime.combine(date.today(), from_time))
    local_to = tz.localize(datetime.combine(date.today(), to_time))

    if local_to <= local_from:
        local_to += timedelta(days=1)

    from_utc = local_from.astimezone(pytz.UTC)
    to_utc = local_to.astimezone(pytz.UTC)

    cursor.execute("DELETE FROM user_availability WHERE user_id=%s", (user["id"],))
    cursor.execute(
        "INSERT INTO user_availability (user_id,from_time,to_time,available_from_utc,available_to_utc) VALUES (%s,%s,%s,%s,%s)",
        (user["id"], data.from_time, data.to_time, from_utc, to_utc)
    )

    conn.commit()
    conn.close()

    return {"message": "Availability set"}
