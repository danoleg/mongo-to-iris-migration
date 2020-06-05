import irisnative
from contextlib import contextmanager
from flask import current_app


class Iris(object):

    def __init__(self):
        ip = "iris"
        port = 51773
        namespace = "USER"
        username = "_SYSTEM"
        password = "demopass"

        connection = irisnative.createConnection(ip, port, namespace, username, password)
        self.dbnative = irisnative.createIris(connection)

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
def iris_connection():
    # create connection to IRIS
    connect = Iris()
    try:
        yield connect
    finally:
        # close connection to IRIS
        connect.close()
