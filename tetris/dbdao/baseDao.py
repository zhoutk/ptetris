from tetris.dbdao import dbhelper

class BaseDao(object):

    def select(self, table, params={}, fields=[]):
        return dbhelper.select(table, params)

    def insert(self, table, params={}, fields=[]):
        if '_id_' in params and len(params) < 2 or '_id_' not in params and len(params) < 1:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.insert(table, params)

    def update(self, table, params={}, fields=[]):
        if '_id_' not in params or len(params) < 2:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.update(table, params)

    def delete(self, table, params={}, fields=[]):
        if '_id_' not in params:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.delete(table, params)

    def querySql(self, values = [], params = {}, fields = []):
        pass

    def execSql(self, sql, values = []):
        return dbhelper.exec_sql(sql, values)

    def insertBatch(self, table, elements = []):
        pass

    def transGo(elements = [], isAsync = False):
        pass
