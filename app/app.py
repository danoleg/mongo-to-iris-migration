import json
import pymongo
import ssl

from flask_restful import Api, Resource, reqparse
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from helpers.encoder import DateTimeEncoder
from helpers.iris import iris_connection
from helpers.parser import parse_dict
from importer import mongo_to_iris, json_to_iris

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

app.config['mongo_connection_string'] = "mongodb://mongodb:27019"
app.config['mongo_db'] = "demo"
app.config['iris_host'] = "iris"
app.config['iris_port'] = 51773
app.config['iris_namespace'] = "USER"
app.config['iris_username'] = "_SYSTEM"
app.config['iris_password'] = "demopass"


class MongoCollections(Resource):
    def get(self):
        client = pymongo.MongoClient(app.config['mongo_connection_string'])
        db = client[app.config['mongo_db']]

        collections = []

        cursor = db.command({"listCollections": 1.0})
        for collection in cursor['cursor']['firstBatch']:
            c = db[collection['name']]
            collections.append({
                "name": collection['name'],
                "count": c.count_documents({})
            })

        data = {
            "collections": collections
        }

        return data, 200, {'Access-Control-Allow-Origin': '*'}


class MongoCollection(Resource):
    def get(self, collection_name):
        client = pymongo.MongoClient(app.config['mongo_connection_string'])
        db = client[app.config['mongo_db']]

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

            return data


class ImportJsonFileToIris(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('json')
        args = post_parser.parse_args()

        # if file:
        result = {
            "result": [args.name,args.json]
        }
        return result


class ImportCustomJsonToIris(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('json')
        args = post_parser.parse_args()

        result, iris_data = json_to_iris(args.json, args.name)
        if result:
            data = {
                "status": True,
                "message": "Imported successfully",
                "global_name": args.name,
                "json_body": args.json,
                "iris_data": iris_data
            }
        else:
            data = {
                "status": False,
                "message": "Invalid json",
                "global_name": args.name,
                "json_body": args.json,
                "iris_data": []
            }

        return data


class CheckGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('node')
        args = post_parser.parse_args()
        with iris_connection() as iris:
           iris_root_nodes_count = iris.count_root_nodes(args.name)
        data = {
            "status": True,
            "data": iris_root_nodes_count
        }

        return data


class DeleteGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        args = post_parser.parse_args()
        result = kill_iris_global(args.name)
        if result:
            data = {
                "status": True,
                "message": f"{args.name} removed successfully",
            }
        else:
            data = {
                "status": False,
                "message": "Error"
            }

        return data


class Settings(Resource):
    def get(self):
        data={
            "mongo_connection_string": app.config['mongo_connection_string'],
            "mongo_db": app.config['mongo_db'],
            "iris_host": app.config['iris_host'],
            "iris_port": app.config['iris_port'],
            "iris_namespace": app.config['iris_namespace'],
            "iris_username": app.config['iris_username'],
            "iris_password": app.config['iris_password']
        }
        return data


class MongoDBSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('mongo_connection_string')
        post_parser.add_argument('mongo_db')
        args = post_parser.parse_args()
        app.config['mongo_connection_string'] = args.mongo_connection_string
        app.config['mongo_db'] = args.mongo_db

        data = {
            "result": "Success"
        }
        return data


class IRISSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('iris_host')
        post_parser.add_argument('iris_port')
        post_parser.add_argument('iris_namespace')
        post_parser.add_argument('iris_username')
        post_parser.add_argument('iris_password')
        args = post_parser.parse_args()
        app.config['iris_host'] = args.iris_host
        app.config['iris_port'] = int(args.iris_port)
        app.config['iris_namespace'] = args.iris_namespace
        app.config['iris_username'] = args.iris_username
        app.config['iris_password'] = args.iris_password

        data = {
            "result": "Success"
        }
        return data


class MongoToIris(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('collection_name')
        args = post_parser.parse_args()
        _, iris_data = mongo_to_iris(args.collection_name)

        data = {
            "result": args.collection_name,
            "iris_data": iris_data,
        }
        with iris_connection() as iris:
            data['iris_root_nodes_count'] = iris.count_root_nodes(args.collection_name)
        return data


api.add_resource(MongoCollections, '/mongodb-collections')
api.add_resource(MongoCollection, '/mongodb-collections/<string:collection_name>')
api.add_resource(MongoToIris, '/mongodb-collections/to-iris')
api.add_resource(ImportJsonFileToIris, '/import-json-file-to-iris')
api.add_resource(ImportCustomJsonToIris, '/import-custom-json-to-iris')
api.add_resource(DeleteGlobal, '/remove-global-from-iris')
api.add_resource(CheckGlobal, '/check-global-from-iris')
api.add_resource(MongoDBSettings, '/settings/mongodb')
api.add_resource(IRISSettings, '/settings/iris')
api.add_resource(Settings, '/settings')


def kill_iris_global(root_item):
    with iris_connection() as iris:
        iris.kill(root_item)
    return 1

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011)
