import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading 
import datetime as dt
import numpy as np


cred = credentials.Certificate("/Users/alex/Downloads/VS Code/project-argus/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
members_ref = db.collection(u'members')
history_ref = db.collection(u'history')
settings_ref = db.collection(u'settings')
# Create a callback on_snapshot function to capture changes
class Encodings():
    def __init__(self):
        self.encodings = []
        self.names = []
       
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

encoding = Encodings()
encoding.update()

listener = threading.Event()
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            encoding.update()
        elif change.type.name == 'MODIFIED':
            print(f'Modified {change.document.id}')
            encoding.update()
        elif change.type.name == 'REMOVED':
            encoding.update()
            print(f'Removed {change.document.id}')
            listener.set()
    print(changes)

col_query =  members_ref

query_watch = col_query.on_snapshot(on_snapshot)
class Members(object):
    def __init__(self, name, access = 3, image = []):
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

    def update_member(id, name, access):
        update_ref = members_ref.document(id)
        if (name != "" and access != ""):
            update_ref.update({
                u'name': name,
                u'access': int(access)
            })
        elif (name != ""):
            update_ref.update({
                u'name':name
            })
        elif (access != ""):
            update_ref.update({
                u'access': int(access)
            })
    
    def __repr__(self):
        return(
            f'Members(\
                name={self.name}, \
                access={self.access}, \
                lastUpdated={self.lastUpdated}, \
                lastAccess={self.lastAccess}\
            )'
        )
class History():
    def __init__(self):
        self.lastLog = history_ref.document(u'most_recent').get().get(u'most_recent_log')

    def check_limit(self):
        return int(dt.datetime.now().strftime("%Y%m%d%H%M%S")) >= self.lastLog[0].get("date")

    def add_history(self, id):
        self.lastLog = []
        for identity in id:
            member = members_ref.document(identity).get()
            self.lastLog.append({
                    u'id': identity,
                    u'name': member.get("name"),
                    u'access': member.get("access"),
                    u'date': int(dt.datetime.now().strftime("%Y%m%d%H%M%S")),
                    u'locked': False
                })
                # history_ref.add(self.lastLog)
        history_ref.document(u'most_recent').set({'most_recent_log':self.lastLog})
        # print(self.lastLog.get("date"))

history_log = History()    

# history_log.add_history(['N6bchCXVzP1e6m4SA9qs', 'vUR4AGbeVdLoNm9OSJSi'])

def config_camera_interval(cameraDuration):
    settings_ref.document(u'configurations').set({u'cameraDuration':cameraDuration})

def add_member(name, access, encoding):
    members_ref.add(Members(name, access, encoding).to_dict())


