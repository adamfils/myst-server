import firebase_admin
from firebase_admin import db, messaging, credentials
from pydantic import BaseModel


class RoomRequest(BaseModel):
    uid: str
    female: bool
    country: str


class RoomUtils:
    @staticmethod
    def get_room(request: RoomRequest):
        FBUtil.init_firebase()
        lobby_users = db.reference('lobby').get()
        print('Lobby Users: ------------------')
        print(lobby_users)

    @staticmethod
    def enter_lobby(request: RoomRequest):
        FBUtil.init_firebase()
        data = {
            'uid': request.uid,
            'female': request.female,
            'country': request.country,
            'available': True,
            'ping': StringUtils.get_time()
        }
        db.reference('lobby').child(request.uid).update(data)

    @staticmethod
    def leave_lobby(request: RoomRequest):
        FBUtil.init_firebase()
        db.reference('lobby').child(request.uid).delete()


class FBUtil:
    @staticmethod
    def init_firebase():
        try:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred, {'databaseURL': 'https://myst-app-default-rtdb.firebaseio.com/'})
        except ValueError:
            firebase_admin.get_app()


class StringUtils:
    @staticmethod
    def get_time():
        import time
        return str(int(round(time.time() * 1000)))

    @staticmethod
    def toBase64(txt: str):
        import base64
        return base64.b64encode(txt.encode())

    @staticmethod
    def fromBase64(txt: str):
        import base64
        return base64.b64decode(txt).decode()
