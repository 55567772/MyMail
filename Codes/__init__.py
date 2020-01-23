# coding: utf-8
import sqlite3


# sqlite返回字典型数据的工厂函数
def dict_factory(cursor, row):
    db_format = {}
    for idx, col in enumerate(cursor.description):
        db_format[col[0]] = row[idx]
    return db_format


def db():
    con = sqlite3.connect("DB/db.sqlite3")
    con.row_factory = dict_factory
    cur = con.cursor()
    return cur
