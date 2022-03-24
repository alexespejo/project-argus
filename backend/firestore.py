import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading 
import datetime as dt
import numpy as np


cred = credentials.Certificate("/Users/alex/Downloads/VS Code/project-argus/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
#create references for database collections 
members_ref = db.collection(u'members')
history_ref = db.collection(u'history')
settings_ref = db.collection(u'settings')


#async listener 
#updates the Encodings class for the  camera 
listener = threading.Event()
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            encoding.update()
            print(change.document.id)
        elif change.type.name == 'REMOVED':
            encoding.update()
            print(f'Removed {change.document.id}')
            listener.set()
    print(changes)
col_query =  members_ref
query_watch = col_query.on_snapshot(on_snapshot)


class Encodings():  #initializes the encodings and names for the camera to read 
    def __init__(self):
        self.encodings = []
        self.names = []
       
    #updates the encodings and names on every update 
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
#initalizes encoding methods 
encoding = Encodings()
encoding.update()

class Members(object): #creates a member for the database 
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
    #update member settings 
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


class History(): #methods to interact with history collection 
    def __init__(self):
        self.lastLog = history_ref.document(u'most_recent').get().get(u'most_recent_log')

    def check_limit(self):
        return int(dt.datetime.now().strftime("%Y%m%d%H%M%S")) >= self.lastLog[0].get("timeStamp") + get_config_camera_interval().get('cameraDuration')

    def add_history(self, id):
        self.lastLog = []
        for identity in id:
            member = members_ref.document(identity).get()
            self.lastLog.append({
                    u'id': identity,
                    u'name': member.get("name"),
                    u'access': member.get("access"),
                    u'timeStamp': int(dt.datetime.now().strftime("%Y%m%d%H%M%S")),
                    u'locked': False
                })
            members_ref.document(identity).update({u'lastAccess': dt.datetime.now()})
        
        history_ref.document(u'most_recent').set({'most_recent_log':self.lastLog})
        history_ref.add({
            u'date': int(dt.datetime.now().strftime("%Y%m%d%H%M%S")),
            u'history': self.lastLog})
        # print(self.lastLog.get("date"))

history_log = History()    

        #update settings
def config_camera_interval(cameraDuration):
    settings_ref.document(u'configurations').set({u'cameraDuration':cameraDuration})

def get_config_camera_interval():
    return  settings_ref.document(u'configurations').get().to_dict()

# print(get_config_camera_interval())
# print(history_log.check_limit())


#add member to the database 
def add_member(name, access, encoding):
    members_ref.add(Members(name, access, encoding).to_dict())


