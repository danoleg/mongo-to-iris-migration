import json

import pymongo
from flask import Flask, redirect, render_template
from helpers.encoder import DateTimeEncoder
from helpers.iris import Iris
from importer import mongo_to_iris

app = Flask(__name__, template_folder='views')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<string:collection_name>')
def info(collection_name):
    # mongo_to_iris('restaurants')
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

        if collection.count() > 0:
            first_doc = collection.find_one()
            if '_id' in first_doc:
                first_doc['_id'] = str(first_doc['_id'])
            data['first_doc'] = json.dumps(first_doc, indent=2, cls=DateTimeEncoder)

        iris = Iris()
        data['iris_root_nodes_count'] = iris.count_root_nodes(collection_name)

        return render_template('main.html', data=data)


@app.route('/<string:collection_name>/move-mongo-to-iris-globals')
def move_to_iris_global(collection_name):
    mongo_to_iris(collection_name)
    return redirect(f'/{collection_name}')


@app.route('/<string:root_item>/kill-iris-global')
def kill_iris_global(root_item):
    iris = Iris()
    iris.kill(root_item)
    return redirect(f'/{root_item}')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011)
