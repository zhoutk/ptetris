from tkinter.constants import NO
from typing import List
from tetris.dbdao import dbhelper

class BaseDao(object):

    def select(self, tablename, params={}, fields=None):
        fields = [] if fields == None else fields
        return dbhelper.select(tablename, params, fields)

    def insert(self, tablename, params={}, fields=[]):
        if '_id_' in params and len(params) < 2 or '_id_' not in params and len(params) < 1:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.insert(tablename, params)

    def update(self, tablename, params={}, fields=[]):
        if '_id_' not in params or len(params) < 2:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.update(tablename, params)

    def delete(self, tablename, params={}, fields=[]):
        if '_id_' not in params:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.delete(tablename, params)

    def querySql(self, sql, values = [], params = {}, fields = []):
        return dbhelper.querySql(sql, values, params, fields)

    def execSql(self, sql, values = []):
        return dbhelper.exec_sql(sql, values)

    def insertBatch(self, tablename, elements : List):
        return dbhelper.insertBatch(tablename,elements)

    def transGo(elements = [], isAsync = False):
        pass
