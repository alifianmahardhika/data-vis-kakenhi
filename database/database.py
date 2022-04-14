import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

def load_db():
    # connect to cluster
    if os.getenv("DB_URL"):
        conn_string = str(os.environ.get("DB_URL"))

    # print(conn_string)
    print('Connecting to cluster')
    client = pymongo.MongoClient(conn_string)

    if os.getenv("DB_NAME"):
        db_name = str(os.environ.get("DB_NAME"))
    # connect to db
    db = client[db_name]

    return db

def load_researchers():
    db = load_db()

    if os.getenv("RESEARCHER_COLLECTION"):
        coll_name = str(os.environ.get("RESEARCHER_COLLECTION"))

    # get collection
    researcher_profiles = db[coll_name]

    return researcher_profiles