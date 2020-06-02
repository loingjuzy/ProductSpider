import pymongo


def saveData(datadict):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['test']
    collection = db['students']
    result = collection.insert(datadict)
    print(result)
