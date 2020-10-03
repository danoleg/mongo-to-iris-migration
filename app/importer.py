import pymongo

from flask import current_app
from helpers.iris import iris_connection
from helpers.parser import parse_dict
from helpers.validator import validate_json


def mongo_to_iris(collection_name: str):

    client = pymongo.MongoClient(current_app.config['mongo_connection_string'])
    db = client[current_app.config['mongo_db']]

    if collection_name not in db.list_collection_names():
        return False, None

    collection = db[collection_name]
    cursor = collection.find({})
    i = 0
    iris_first_node = []

    with iris_connection() as iris:
        for document in cursor:
            document['_id'] = str(document['_id'])
            iris_comp_data = parse_dict(document)
            if i == 0:
                iris_first_node = iris_comp_data
            for item in iris_comp_data:
                path_list = [i]+item['path_list']
                iris.set(item['value'], collection_name, *path_list)
            i += 1
        return True, iris_first_node


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





