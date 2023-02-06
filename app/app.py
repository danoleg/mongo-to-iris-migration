import json
import pymongo
import ssl
import psycopg2

from flask_restful import Api, Resource, reqparse
from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from flask_cors import CORS
from helpers.encoder import DateTimeEncoder
from helpers.iris import iris_connection
from helpers.parser import parse_dict
from helpers.postgres import get_table_data
from helpers.iris_export import grab_data, generate_tree
from importer import mongo_to_iris, json_to_iris

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

app.config['mongo_connection_string'] = "mongodb://mongodb:27019"
app.config['mongo_db'] = "demo"
app.config['iris_host'] = "iris"
app.config['iris_port'] = 1972
app.config['iris_namespace'] = "USER"
app.config['iris_username'] = "_SYSTEM"
app.config['iris_password'] = "demopass"

app.config['postgres_host'] = "pgdb"
app.config['postgres_port'] = 5432
app.config['postgres_db'] = "postgres"
app.config['postgres_username'] = "postgres"
app.config['postgres_password'] = "postgres"

app.config['upload_folder'] = 'static'


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
                "docs_count": collection.count_documents({})
            }

            with iris_connection() as iris:
                data['iris_root_nodes_count'] = iris.count_root_nodes(collection_name)

            if collection.count_documents({}) > 0:
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


class ExportGlobalToJson(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('json')
        args = post_parser.parse_args()

        with iris_connection() as iris:
            data = grab_data(iris, args.name, *tuple())
            data = generate_tree(data)

        result = {
            "result": data
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
            "iris_password": app.config['iris_password'],
            "postgres_host": app.config['postgres_host'],
            "postgres_port": app.config['postgres_port'],
            "postgres_db": app.config['postgres_db'],
            "postgres_username": app.config['postgres_username'],
            "postgres_password": app.config['postgres_password']
        }
        return data


class MongoDBSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('mongo_connection_string')
        post_parser.add_argument('mongo_db')
        args = post_parser.parse_args()

        try:
            client = pymongo.MongoClient(args.mongo_connection_string)
            db = client[args.mongo_db]
            cursor = db.command({"listCollections": 1.0})
        except Exception as e:
            data = {
                "result": "Error",
                "details": str(e)
            }
            return data

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

        try:
            connection = args.iris_host, int(args.iris_port), args.iris_namespace, args.iris_username, args.iris_password
            with iris_connection(*connection) as iris:
                pass
        except Exception as e:
            data = {
                "result": "Error",
                "details": str(e)
            }
            return data

        app.config['iris_host'] = args.iris_host
        app.config['iris_port'] = int(args.iris_port)
        app.config['iris_namespace'] = args.iris_namespace
        app.config['iris_username'] = args.iris_username
        app.config['iris_password'] = args.iris_password

        data = {
            "result": "Success"
        }
        return data


class PostgresSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('postgres_host')
        post_parser.add_argument('postgres_port')
        post_parser.add_argument('postgres_db')
        post_parser.add_argument('postgres_username')
        post_parser.add_argument('postgres_password')
        args = post_parser.parse_args()

        try:
            conn = psycopg2.connect(
                dbname=args.postgres_db,
                user=args.postgres_username,
                password=args.postgres_password,
                host=args.postgres_host,
                port=int(args.postgres_port),
            )
            cur = conn.cursor()
            cur.close()
            conn.close()
        except Exception as e:
            data = {
                "result": "Error",
                "details": str(e)
            }
            return data

        app.config['postgres_host'] = args.postgres_host
        app.config['postgres_port'] = int(args.postgres_port)
        app.config['postgres_db'] = args.postgres_db
        app.config['postgres_username'] = args.postgres_username
        app.config['postgres_password'] = args.postgres_password

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


class PostgesTables(Resource):
    def get(self):
        conn = psycopg2.connect(
            dbname=app.config['postgres_db'],
            user=app.config['postgres_username'],
            password=app.config['postgres_password'],
            host=app.config['postgres_host'],
            port=app.config['postgres_port'],
        )

        cur = conn.cursor()
        cur.execute("SELECT tablename FROM pg_catalog.pg_tables where schemaname = 'public';")
        d = cur.fetchall()
        # field_names = [i[0] for i in cur.description]
        collections = []
        with iris_connection() as iris:
            for i in d:
                collections.append({
                    "name": i[0]
                })

        cur.close()
        conn.close()

        data = {
            "collections": collections
        }

        return data, 200, {'Access-Control-Allow-Origin': '*'}


class PostgesTable(Resource):
    def get(self, table_name):
        conn = psycopg2.connect(
            dbname=app.config['postgres_db'],
            user=app.config['postgres_username'],
            password=app.config['postgres_password'],
            host=app.config['postgres_host'],
            port=app.config['postgres_port'],
        )
        cur = conn.cursor()

        collection, count, field_names, row_data = get_table_data(table_name, cur, limit=10)

        cur.close()
        conn.close()

        if collection is False:
            return f"Table '{table_name}' not found"
        else:

            data = {
                "fields": field_names,
                "collection_name": table_name,
                "docs_count": count
            }

            with iris_connection() as iris:
                data['iris_root_nodes_count'] = iris.count_root_nodes(table_name)

            if count > 0:
                data['table_data'] = [list(i) for i in row_data]

                if data['iris_root_nodes_count'] > 0:
                    data['iris_data'] = parse_dict(collection)

            return data


class PostgresToIris(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        args = post_parser.parse_args()

        conn = psycopg2.connect(
            dbname=app.config['postgres_db'],
            user=app.config['postgres_username'],
            password=app.config['postgres_password'],
            host=app.config['postgres_host'],
            port=app.config['postgres_port'],
        )
        cur = conn.cursor()
        collection, count, _, _ = get_table_data(args.name, cur)


        result, iris_data = json_to_iris(json.dumps(collection), args.name)

        collection, count, _, _ = get_table_data(args.name, cur, limit=10)

        cur.close()
        conn.close()

        if result:
            data = {
                "status": True,
                "message": "Imported successfully",
                "global_name": args.name,
                "iris_data": parse_dict(collection),
                "iris_root_nodes_count": count,
            }
        else:
            data = {
                "status": False,
                "message": "Invalid json",
                "global_name": args.name,
                "iris_data": parse_dict(collection),
                "iris_root_nodes_count": 0
            }

        return data


api.add_resource(MongoCollections, '/mongodb-collections')
api.add_resource(MongoCollection, '/mongodb-collections/<string:collection_name>')
api.add_resource(PostgesTable, '/postgresql-tables/<string:table_name>')
api.add_resource(MongoToIris, '/mongodb-collections/to-iris')
api.add_resource(PostgresToIris, '/postgresql-tables/to-iris')
api.add_resource(PostgesTables, '/postgresql-tables')
api.add_resource(ImportJsonFileToIris, '/import-json-file-to-iris')
api.add_resource(ImportCustomJsonToIris, '/import-custom-json-to-iris')
api.add_resource(ExportGlobalToJson, '/export-iris-to-json')
api.add_resource(DeleteGlobal, '/remove-global-from-iris')
api.add_resource(CheckGlobal, '/check-global-from-iris')
api.add_resource(MongoDBSettings, '/settings/mongodb')
api.add_resource(IRISSettings, '/settings/iris')
api.add_resource(PostgresSettings, '/settings/postgres')
api.add_resource(Settings, '/settings')


def kill_iris_global(root_item):
    with iris_connection() as iris:
        iris.kill(root_item)
    return 1


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011, debug=True)
