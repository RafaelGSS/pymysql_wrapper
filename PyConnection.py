import pymysql


class MysqlConnectException(Exception):
    pass


class MysqlQueryException(Exception):
    pass


class PySession(object):
    def __init__(self, host, user, password, database, port):
        self.connected = False
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
        self.__connection = self.session()

    def session(self):
        try:
            db = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__database,
                                 port=self.__port, cursorclass=pymysql.cursors.DictCursor, connect_timeout=30)
            db.autocommit(True)
            self.connected = True
            return db
        except MysqlConnectException as e:
            print(str(e))
            self.connected = False
            return None

    def query(self, query, fetch_all=True):
        if self.connected is False:
            return None
        try:
            with self.__connection.cursor() as cursor:
                rows = cursor.execute(query)
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Exception as e:
            print(str(e))
            self.connected = False
            return None

    def query_returning_rows(self):
        pass


class PyConnection(object):
    def __init__(self, host, user, password, database, name, port=3306, connections=1):
        self.__connection_pool = {}
        self.__default_pool = name
        self.add_multiple_connections(host, user, password, database, name, port, connections)

    def execute(self, query, name_pool=None, fetch_all=True):
        if name_pool is None:
            name_pool = self.__default_pool

        response = ''
        try:
            for conn in self.__connection_pool[name_pool]:
                if conn.connected:
                    res = conn.query(query)
                    if res is None and conn.connected is False:
                        continue
                    response = res
                    break
            return response
        except Exception as e:
            print(str(e))
            return None

    def execute_get_rows(self, query, name_pool=None):
        pass

    def thread_reconnect(self):
        pass

    def set_default_name_pool(self, name):
        self.__default_pool = name

    def add_new_connection(self, host, user, password, database, name, port):
        self.__connection_pool[name].append(PySession(host, user, password, database, port))

    def add_multiple_connections(self, host, user, password, database, name, port, connections):
        for i in range(0, connections):
            self.add_new_connection(host, user, password, database, name, port)


