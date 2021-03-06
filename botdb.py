import json, os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Update cert file with secrets
certFile = 'keys/dragonbot-discord-bca65b7a592f.json'
with open(certFile) as f:
  data = json.load(f)
pkey = os.environ.get("FIREBASE_PRIVATE_KEY")
pkey = pkey.replace('\\n', "\n")
data['private_key'] = pkey
with open(certFile, 'w') as f:
  json.dump(data, f)

# Use a service account
cred = credentials.Certificate(certFile)
firebase_admin.initialize_app(cred)

_db = firestore.client()

def set(key, data, collection="default"):
  doc_ref = _db.collection(collection).document(key)
  doc_ref.set(data)

def get(key, collection="default"):
  try:
    if not key:
      if collection != "default":
        # return many
        doc_ref = _db.collection(collection)
        docs = doc_ref.get()
        records = []
        for doc in docs:
          docs.append(doc.to_dict())
        return records
      else:
        # don't allow this
        return None

    # return one
    doc_ref = _db.collection(collection).document(key)
    doc = doc_ref.get()
    return doc.to_dict()
  except:
    pass

  return None
