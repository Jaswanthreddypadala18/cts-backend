from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import auth
import groups
import profile
import availability
import notifications
from scheduler import start_scheduler


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(profile.router)
app.include_router(availability.router)
app.include_router(notifications.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()

