import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import datetime as dt
import numpy as np


cred = credentials.Certificate(
    "/Users/alex/Downloads/VS Code/project-argus/fir-py-c779c-firebase-adminsdk-gmpay-0f1a3c1852.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# create references for database collections
members_ref = db.collection(u'members')
history_ref = db.collection(u'history')
settings_ref = db.collection(u'settings')


class Encodings():  # initializes the encodings and names for the camera to read
    def __init__(self):
        self.encodings = []
        self.names = []
    # updates the encodings and names on every update

    def update(self):
        self.encodings = []
        self.names = []
        for member in members_ref.stream():
            self.names.append(member.id)
            self.encodings.append(np.array(member.to_dict().get("image")))

    def get_encodings(self):
        return self.encodings

    def get_names(self):
        return self.names


# initalizes encoding methods
encoding = Encodings()
encoding.update()


def create_time_dict():  # create date dict
    return {
        u'month': 30 * int(dt.datetime.now().strftime("%m")),
        u'day':  int(dt.datetime.now().strftime("%d")),
        u'year':  int(dt.datetime.now().strftime("%Y")),
        u'hour': 60 * int(dt.datetime.now().strftime("%H")),
        u'minute':  int(dt.datetime.now().strftime("%M")),
        u'seconds':  int(dt.datetime.now().strftime("%S"))
    }


class settings:
    def __init__(self):
        self.camera_duration = db.collection(u'settings').document(
            u'configurations').get().get(u'cameraDuration')
        self.door_locked = db.collection(
            u'settings').document(u'locked').get().get(u'door')

    def update_settings(self):
        self.camera_duration = db.collection(u'settings').document(
            u'configurations').get().get(u'cameraDuration')
        self.door_locked = db.collection(
            u'settings').document(u'locked').get().get(u'door')

    def get_duration(self):
        return self.camera_duration

    def get_door(self):
        return self.door_locked


camera_settings = settings()


class Members(object):  # creates a member for the database
    def __init__(self, name, access=3, image=[]):
        self.name = name
        self.image = image
        self.access = access
        self.lastUpdated = dt.datetime.now()
        self.lastAccess = None

    def to_dict(self):
        return {
            "name": self.name,
            "access": self.access,
            "lastUpdated": self.lastUpdated,
            "lastAccess": self.lastAccess,
            "image": self.image
        }


class History():  # methods to interact with history collection
    def __init__(self):
        self.lastLog = history_ref.document(
            u'most_recent').get().get(u'most_recent_log')
        self.lastPerson = history_ref.document(
            u'most_recent').get().get(u'most_recent_log')[0].get('name')
        self.door = camera_settings.get_door()

    def update_door(self):
        self.door = camera_settings.get_door()

    def get_most_recent_member(self):
        return self.lastPerson

    def get_most_recent_time(self):
        return self.lastLog

    def add_history(self, id):
        self.lastLog = []

        for identity in id:
            if (identity == "unknown"):
                self.lastLog.append({
                    u'id': "unknown",
                    u'name': "unknown",
                    u'access': "unknown",
                    u'timeStamp': create_time_dict(),
                    u'locked': self.door
                })
            else:
                member = members_ref.document(identity).get()
                self.lastLog.append({
                    u'id': identity,
                    u'name': member.get("name"),
                    u'access': member.get("access"),
                    u'timeStamp': create_time_dict(),
                    u'locked': self.door
                })
                members_ref.document(identity).update(
                    {u'lastAccess': create_time_dict()})

        history_ref.document(u'most_recent').set(
            {'most_recent_log': self.lastLog})
        history_ref.add({
            u'date': int(dt.datetime.now().strftime("%Y%m%d%H%M%S")),
            u'history': self.lastLog})


history_log = History()
# history_log.add_history(['dGNMh2LtzNAxtpjtVbZg', 'unknown'])
# print(history_log.get_most_recent_member())


def config_camera_interval(cameraDuration):
    settings_ref.document(u'configurations').set(
        {u'cameraDuration': cameraDuration})


def get_config_camera_interval():
    return settings_ref.document(u'configurations').get().to_dict().get('cameraDuration')

# add member to the database


def add_member(name, access, encoding):
    members_ref.document(f"{name}{access}").set(
        Members(name, access, encoding).to_dict())

    # update member settings


def update_member(id, name, access):
    update_ref = members_ref.document(id)
    if (name != "" and access != ""):
        update_ref.update({
            u'name': name,
            u'access': int(access)
        })
    elif (name != ""):
        update_ref.update({
            u'name': name
        })
    elif (access != ""):
        update_ref.update({
            u'access': int(access)
        })


# async listener
# updates the Encodings class for the  camera
listener = threading.Event()


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            print("update made")
            encoding.update()
            camera_settings.update_settings()
            history_log.update_door()
            print(camera_settings.get_door())
            print(f"HISTORY DOOR {history_log.door}")
            # print(change.document.id)
        elif change.type.name == 'REMOVED':
            encoding.update()
            print(f'Removed {change.document.id}')
            listener.set()
    print(changes)


member_watch = members_ref.on_snapshot(on_snapshot)
settings_watch = settings_ref.on_snapshot(on_snapshot)
