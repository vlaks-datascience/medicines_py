# import os
from pymongo import MongoClient

### this is for docker 
# mongo_uri = os.environ.get('MONGO_URI')
# if not mongo_uri:
#     raise ValueError('No MongoDB URI configured')

conn = MongoClient('mongodb://localhost:27017/test')
