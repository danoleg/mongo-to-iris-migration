import pymongo

from helpers.iris import iris_connection
from helpers.parser import parse_dict
from helpers.validator import validate_json


def mongo_to_iris(collection_name: str):

    client = pymongo.MongoClient("mongodb", 27019)
    db = client.demo

    if collection_name not in db.list_collection_names():
        return False, None

    collection = db[collection_name]
    cursor = collection.find({})
    i = 0

    with iris_connection() as iris:
        for document in cursor:
            document['_id'] = str(document['_id'])
            iris_comp_data = parse_dict(document)
            for item in iris_comp_data:
                path_list = [i]+item['path_list']
                iris.set(item['value'], collection_name, *path_list)
            i += 1
        return True, iris_comp_data[0]


def json_to_iris(input_data: str, global_name: str) -> tuple:

    data, status = validate_json(input_data)
    if not status:
        return False, None
    else:
        with iris_connection() as iris:
            iris_comp_data = parse_dict(data)
            for item in iris_comp_data:
                path_list = item['path_list']
                iris.set(item['value'], global_name, *path_list)
            return True, iris_comp_data





