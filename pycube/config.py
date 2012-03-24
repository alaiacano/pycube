import pymongo
HTTP_HOST = '127.0.0.1'
DB_CONN = pymongo.Connection(HTTP_HOST).cube_development
COLLECTIONS = DB_CONN.collection_names()
