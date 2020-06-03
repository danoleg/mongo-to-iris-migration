import json

import pymongo
from flask import Flask, redirect, render_template, request, url_for
from helpers.encoder import DateTimeEncoder
from helpers.iris import iris_connection
from helpers.parser import parse_dict
from importer import mongo_to_iris, json_to_iris

app = Flask(__name__, template_folder='views')


@app.route('/')
def home():
    client = pymongo.MongoClient("mongodb", 27019)
    db = client.demo
    data = {
        "collections": db.list_collection_names()
    }
    return render_template('home.html', data=data)


@app.route('/mongodb/<string:collection_name>')
def mongo_collection_info(collection_name):
    client = pymongo.MongoClient("mongodb", 27019)
    db = client.demo

    if collection_name not in db.list_collection_names():
        return f"Collection '{collection_name}' not found"
    else:
        collection = db[collection_name]

        data = {
            "collection_name": collection_name,
            "docs_count": collection.count()
        }

        with iris_connection() as iris:
            data['iris_root_nodes_count'] = iris.count_root_nodes(collection_name)

        if collection.count() > 0:
            first_doc = collection.find_one()
            if '_id' in first_doc:
                first_doc['_id'] = str(first_doc['_id'])
            data['first_doc'] = json.dumps(first_doc, indent=2, cls=DateTimeEncoder)

            if data['iris_root_nodes_count'] > 0:
                data['iris_data'] = parse_dict(first_doc)

        return render_template('main.html', data=data)


@app.route('/mongodb/<string:collection_name>/move-mongo-to-iris-globals')
def move_to_iris_global(collection_name):
    mongo_to_iris(collection_name)
    return redirect(url_for('mongo_collection_info', collection_name=collection_name))


@app.route('/mongodb/<string:root_item>/kill-iris-global')
def kill_iris_global(root_item):
    with iris_connection() as iris:
        iris.kill(root_item)
    return redirect(url_for('mongo_collection_info', collection_name=root_item))


@app.route('/import-json', methods=['GET', 'POST'])
def json_import():
    data = {
        "global_name": "DemoGlobal",
        "json_body": json.dumps({
              "address": {
                "building": "1007",
                "coord": [
                  -73.856077,
                  40.848447
                ],
                "street": "Morris Park Ave",
                "zipcode": "10462"
              },
              "name": "Morris Park Bake Shop",
              "restaurant_id": "30075445"
            }, indent=2)
    }

    if request.method == 'POST':
        global_name = request.form.get('name')
        json_body = request.form.get('json')

        result, iris_data = json_to_iris(json_body, global_name)
        if result:
            data = {
               "status": True,
               "message": "Imported successfully",
               "global_name": global_name,
               "json_body": json_body,
               "iris_data": iris_data
            }
        else:
            data = {
               "status": False,
               "message": "Invalid json",
               "global_name": global_name,
               "json_body": json_body
            }

    return render_template('import_json.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011)
