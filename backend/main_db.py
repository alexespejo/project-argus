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

# Create a callback on_snapshot function to capture changes
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

    def __repr__(self):
        return(
            f'Members(\
                name={self.name}, \
                access={self.access}, \
                lastUpdated={self.lastUpdated}, \
                lastAccess={self.lastAccess}\
            )'
        )

class Encodings():
    def __init__(self):
        self.encodings = []
        self.names = []
       
    def update(self):
        self.encodings = []
        self.names = []
        for member in members_ref.stream():
            self.names.append(member.to_dict().get("name"))
            self.encodings.append(np.array(member.to_dict().get("image")))
       
    def get_encodings(self):
        return self.encodings

    def get_names(self):
        return self.names

encoding = Encodings()
encoding.update()

def add_member(name, access, encoding):
    members_ref.add(Members(name, access, encoding).to_dict())

# history_ref.add(members_ref.document(u'oLAeniVEp4CuYK9NBhFG'))
# for member in members_ref.stream():
#     if member.id == 'oLAeniVEp4CuYK9NBhFG':
#         print(member.to_dict())

print(members_ref.where(u'name', u'==', u'Alex').stream().to_dict())