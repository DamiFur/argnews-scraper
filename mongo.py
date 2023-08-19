import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["tweet-stands"]

def setup(collection):
    try:
        db[collection].create_index(
            [('text', pymongo.TEXT)],
            default_language='spanish')
    except:
        print("index already created")

def store(article, collection):
    db[collection].insert_one(article)

def check_if_exists(query, collection):
    print(dir(db[collection]))
    if db[collection].count(query) > 0:
        return True
    return False