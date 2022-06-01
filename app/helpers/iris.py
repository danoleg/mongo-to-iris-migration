import irisnative
from contextlib import contextmanager
from flask import current_app


class Iris(object):

    def __init__(self, *connection):
        if connection:
            ip, port, namespace, username, password = connection
        else:
            ip = current_app.config['iris_host']
            port = current_app.config['iris_port']
            namespace = current_app.config['iris_namespace']
            username = current_app.config['iris_username']
            password = current_app.config['iris_password']

        self.connection = irisnative.createConnection(ip, port, namespace, username, password)
        self.dbnative = irisnative.createIris(self.connection)

    def set(self, value: any, global_name: str, *nodes):
        """
        Create or update global node value

        :param value:
        :param global_name: root global name
        :param nodes: path to value
        """
        self.dbnative.set(value, global_name, *nodes)

    def get(self, global_name, *nodes):
        """
        Get global node value

        :param global_name: root global name
        :param nodes: path to value
        :return:
        """
        try:
            value = self.dbnative.get(global_name, *nodes)
        except Exception:
            value = None
        return value

    def kill(self, global_name):
        try:
            self.dbnative.kill(global_name)
        except Exception:
            return 0
        return 1

    def count_root_nodes(self, global_name: str) -> int:
        """

        :param global_name: str
        :return: int
        """
        iter = self.dbnative.iterator(global_name)
        return sum(1 for _ in iter.items())

    def close(self):
        """
        Close IRIS connection
        """
        self.connection.close()


@contextmanager
def iris_connection(*connection):
    # create connection to IRIS
    connect = Iris(*connection)
    try:
        yield connect
    finally:
        # close connection to IRIS
        connect.close()
