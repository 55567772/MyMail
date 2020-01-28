# coding: utf-8
from Codes import MSSQL


class WebConfig:
    def __init__(self):
        self.conn = MSSQL()

    # 取出所有承运商，方便给程序调用
    def get_Carders(self):
        tmp_dict = dict()
        sql = "select * from Carder"
        res = self.conn.sDB(sql)
        for row in res:
            tmp_dict[str(row['ID'])] = dict()
            for k, v in row.items():
                tmp_dict[str(row['ID'])][k] = v
        return tmp_dict
