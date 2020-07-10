import sqlite3 as sql
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "flask.db")

def connectTo():
    with sql.connect(db_path) as con:
        cur = con.cursor()
        return cur

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_json(selsql):
    con = sql.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(selsql)
    rows = cur.fetchall()
    return rows

def selectId_json(selsql,idTable):
    con = sql.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(selsql,idTable)
    rows = cur.fetchall()
    return rows

def select(selsql):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(selsql)
    x = cur.fetchall()
    return x

def selectId(selsql,idTable):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(selsql,idTable)
    x = cur.fetchall()
    return x

def insert(selsql):
    with sql.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(selsql)
        return con.commit()

def cud(selsql,dataForm):
    with sql.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(selsql,dataForm)
        return con.commit()

