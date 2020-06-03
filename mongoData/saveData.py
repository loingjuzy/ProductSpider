import pymongo


client = pymongo.MongoClient(host='localhost', port=27017)


def saveData(datadict, db, collection):
    result = client[db][collection].insert(datadict)
    print(result)
