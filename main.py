import os
import ssl
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from firebase_admin import credentials, db, messaging
import firebase_admin

from utils import RoomRequest, FBUtil, RoomUtils, StringUtils

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://myst-app-default-rtdb.firebaseio.com/'})
os.chdir(os.path.dirname(__file__))
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()


@app.get("/")
def root(request: Request):
    host = request.client.host
    print(StringUtils.get_time())
    return StringUtils.toBase64(host)


@app.post("/room")
def join_room(request: Request, room_request: RoomRequest):
    host = request.client.host
    if room_request.uid is None:
        raise HTTPException(status_code=400, detail="UID is required")
    user = db.reference('users').child(room_request.uid).get()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    print(user)
    RoomUtils.enter_lobby(room_request)
    RoomUtils.get_room(room_request)

    return str()
