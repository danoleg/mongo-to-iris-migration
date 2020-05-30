import pymongo

from helpers.iris import Iris
from helpers.parser import parse_dict


def mongo_to_iris(collection_name: str):

    iris = Iris()

    client = pymongo.MongoClient("mongodb", 27019)
    db = client.demo

    if collection_name not in db.list_collection_names():
        return 0

    collection = db[collection_name]
    cursor = collection.find({})
    i = 0
    for document in cursor:
        document['_id'] = str(document['_id'])
        iris_comp_data = parse_dict(document)
        for item in iris_comp_data:
            path_list = [i]+item['path_list']
            iris.set(item['value'], collection_name, *path_list)
        i += 1
    return 1
