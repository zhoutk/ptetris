import sqlite3 as dbHandle
import os

def exec_sql(sql, values, opType = 0):
    try:
        flag = False
        error = {}
        if not os.path.exists("./dist"):
            os.mkdir("dist")
        conn = dbHandle.connect("./dist/log.db")
        cur = conn.cursor()
        if opType == 1:
            num = cur.executemany(sql, values)
        else:
            num = cur.execute(sql, values)
        if opType == 2:
            result = cur.fetchall()
        else:
            conn.commit()
        print('Sql: ', sql, ' Values: ', values)
    except Exception as err:
        flag = True
        error = err
        print('Error: ', err)
    finally:
        conn.close()
        if flag:
            return False, error, num if 'num' in dir() else 0
    return True, result if 'result' in dir() else [], len(result) if opType == 2 else num.rowcount if 'num' in dir() else 0


def delete(tablename, params={}):
    sql = "delete from %s  where _id_ = ? " % tablename
    rs = exec_sql(sql, [params["_id_"]])
    if rs[0]:
        return {"code": 200, "info": "delete success.", "total": rs[2]}
    else:
        return {"code": 401, "error": rs[1].args[0], "total": rs[2]}


def update(tablename, params={}):
    sql = "update %s set " % tablename
    ks = params.keys()
    vs = []
    for al in ks:
        if not al == "_id_":
            sql += "`" + al + "` = ?,"
            vs.append(params[al])
        else:
            idVal = params[al]
    sql = sql[:-1]
    sql += " where _id_ = ? "
    vs.append(idVal)
    rs = exec_sql(sql, vs)
    if rs[0]:
        return {"code": 200, "info": "update success.", "total": rs[2]}
    else:
        return {"code": 402, "error": rs[1].args[0], "total": rs[2]}


def insert(tablename, params={}):
    sql = "insert into %s ( " % tablename
    ks = params.keys()
    vs = []
    ps = ""
    for al in ks:
        sql += al + ","
        ps += "?,"
        vs.append(params[al])
    sql = sql[:-1] + ") values (" + ps[:-1] + ")"
    rs = exec_sql(sql, vs)
    if rs[0]:
        return {"code": 200, "info": "create success.", "total": rs[2]}
    else:
        return {"code": 701, "error": rs[1].args[0], "total": rs[2]}

def querySql(sql, values =[], params ={}, fields = []):
    return select("QuerySqlSelect", params, fields, sql, values)


def select(tablename, params={}, fields=[], sql = "", values = []):
    where = ""
    AndJoinStr = ' and '

    reserveKeys = {}
    for rk in ["sort", "search", "page", "size", "sum", "count", "group"]:
        if params.get(rk):
            reserveKeys[rk] = params[rk]
            params.pop(rk)

    for k, v in params.items():
        if where != '':
            where += AndJoinStr
        whereExtra = ""
        if k == "ins":
            whereExtra += v[0] + " in (%s) " % ','.join('?'*len(v[1:]))
            values += v[1:]
        elif k == "lks" or k == "ors":
            whereExtra = ' ( '
            index = 0
            while index < len(v):
                if index > 0:
                    whereExtra += ' or '
                whereExtra += v[index] + (' like' if k == 'lks' else ' =') + ' ? '
                values.append("%" + v[index + 1] + "%" if k == 'lks' else v[index + 1])
                index += 2
            whereExtra += ' ) '
        else:
            flag = False
            if type(v) == "str":
                vals = v.split(',')
                for condition in ['>','>=','<','<=','==','<>']:
                    if vals[0] == condition:
                        flag = True
                        break
            if flag:
                if len(vals) == 2:
                    where += k + vals[0] + ' ? '
                    values.append(vals[1])
                elif len(vals) == 4:
                    where += k + vals[0] + ' ? and ' + k + vals[2] + ' ? '
                    values.append(vals[1])
                    values.append(vals[3])
                else:
                    if where.endswith(AndJoinStr):
                        where = where[:-len(AndJoinStr)]
            elif reserveKeys.get('search'):
                whereExtra += k + " like ? "
                values.append("%" + v + "%")
            else:
                whereExtra += k + " =? "
                values.append(v)
        where += whereExtra

    extra = ""
    v = reserveKeys.get('sum')
    if v != None:
        extra += ', sum('+ v[0] +') as ' + v[1]
    v = reserveKeys.get('count')
    if v != None:
        extra += ', count('+ v[0] +') as ' + v[1]

    if tablename == 'QuerySqlSelect':
        sql = sql + ('' if where == '' else (' and ' + where))
    else:
        sql = "select %s %s from %s " % ('*' if len(fields) == 0 else ','.join(fields), extra, tablename)
        sql += '' if where == '' else ' WHERE ' + where

    v = reserveKeys.get('group')
    if v != None:
        sql += ' GROUP BY ' + v

    v = reserveKeys.get('sort')
    if v != None:
        sql += ' ORDER BY ' + v

    page = reserveKeys.get('page')
    size = reserveKeys.get('size')
    if not size:
        size = 10
    if page and page > 0:
        page -= 1
        # sql += " LIMIT %d,%d " % (page * size, size)
        sql += f' LIMIT {page * size}, {size}'
        
    rs = exec_sql(sql, values, 2)
    if rs[0]:
        return {"code": 200, "rows": rs[1], "total": rs[2]}
    else:
        return {"code": 602, "error": rs[1].args[0], "total": rs[2]}

def insertBatch(tablename, elements=[]):
    sql = "insert into %s ( " % tablename
    isFirst = True
    vs = []
    ps = ""
    for ele in elements:
        if isFirst:
            isFirst = False
            ks = ele.keys()
            for al in ks:
                sql += al + ","
                ps += "?,"
        items = []
        for bl in ks:
            items.append(ele[bl])
        vs.append(items)
    sql = sql[:-1] + ") values (" + ps[:-1] + ")"
    rs = exec_sql(sql, vs, 1)
    if rs[0]:
        return {"code": 200, "info": "create success.", "total": rs[2]}
    else:
        return {"code": 701, "error": rs[1].args[0], "total": rs[2]}