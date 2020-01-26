# coding: utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from Codes import MSSQL
import json
from xpinyin import Pinyin
from django.shortcuts import redirect

conn = MSSQL()


# 递归获取管理权限
def LoopPur(ParentID, auto_list=list):
    """
        参数说明
        ParentID: 父级ID
        menu: 继承的上级dic
    """
    sql = "Select [ID], [PageName] as title, [PageUrl] as href, [PageIcon] as icon " \
          "From Page_Manager where [ParentID] = {0}".format(ParentID)
    res = conn.sDB(sql)
    for row in res:
        if row['title'] in ['首页', '业务管理']:
            row['isCurrent'] = True
        row['children'] = LoopPur(row['ID'], [])
        auto_list.append(row)
    return auto_list


class GetJSON:
    def __init__(self, args=dict):
        self.args = args
        self.conn = MSSQL()

    # 查询承运商列表
    def aa(self):
        other_sql = "where 1=1 "
        Carder_MarkName = "%s" % self.args.get('Carder_MarkName', '').strip().replace("'", "")
        if Carder_MarkName:
            other_sql += "and Carder_MarkName like '%{0}%'".format(Carder_MarkName)
        sql = 'Select * from Carder {0} order by ID desc'.format(other_sql)
        result = self.conn.sDB(sql)
        return str(json.dumps(result))

    # 添加，修改 承运商
    def ab(self):
        try:
            # 拼音
            ms = MSSQL()
            p = Pinyin()
            if self.args['EditType'] == 'add':
                self.conn.eDB("INSERT INTO Carder(Carder_MarkName, Carder_Mobile, "
                              "Carder_Address, Carder_User, Carder_BankUserName, "
                              "Carder_BankNumber, Carder_BankLive, Carder_Type, Carder_CarNumber, Carder_PY) "
                              "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')"
                              .format(self.args.get('Carder_MarkName', ''),
                                      self.args.get('Carder_Mobile', ''),
                                      self.args.get('Carder_Address', ''),
                                      self.args.get('Carder_User', ''),
                                      self.args.get('Carder_BankUserName', ''),
                                      self.args.get('Carder_BankNumber', ''),
                                      self.args.get('Carder_BankLive', ''),
                                      self.args.get('Carder_Type', ''),
                                      self.args.get('Carder_CarNumber', ''),
                                      p.get_initials(self.args.get('Carder_MarkName', ''), ''))
                       )
            else:
                self.conn.eDB("UPDATE Carder Set Carder_MarkName = '{0}', Carder_Mobile = '{1}', "
                              "Carder_Address = '{2}', Carder_User = '{3}', Carder_BankUserName = '{4}', "
                              "Carder_BankNumber = '{5}', Carder_BankLive = '{6}', Carder_Type = '{7}', "
                              "Carder_CarNumber = '{8}', Carder_PY = '{9}' where ID='{10}'"
                              .format(self.args.get('Carder_MarkName', ''),
                                      self.args.get('Carder_Mobile', ''),
                                      self.args.get('Carder_Address', ''),
                                      self.args.get('Carder_User', ''),
                                      self.args.get('Carder_BankUserName', ''),
                                      self.args.get('Carder_BankNumber', ''),
                                      self.args.get('Carder_BankLive', ''),
                                      self.args.get('Carder_Type', ''),
                                      self.args.get('Carder_CarNumber', ''),
                                      p.get_initials(self.args.get('Carder_MarkName', ''), ''),
                                      self.args.get('ID', ''))
                       )
            return str(json.dumps({"err": False, "data": self.args}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 删除承运商列
    @csrf_exempt
    def ac(self):
        try:
            self.conn.eDB("DELETE FROM Carder WHERE ID = '{0}'".format(int(self.args['ID'])))
            return str(json.dumps({"err": False, "data": "ok"}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 获取不同用户页面权限分配
    @csrf_exempt
    def sa(self):
        all_element = list()
        tmp_children = dict()
        # try:
        sql = "Select [ID], [PageName] as title, [PageUrl] as href, [PageIcon] as icon From Page_Manager where [ParentID] = 0"
        res = conn.sDB(sql)
        for row in res:
            if row['title'] in ['首页', '业务管理']:
                row['isCurrent'] = True
            row['menu'] = LoopPur(row['ID'], [])
            all_element.append(row)
        return "var SystemMenu = " + json.dumps(all_element)

    def lo(self):
        sql = "select count(*) from Carder"
        redirect


@csrf_protect
def redirect(request, key):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET
    if not key:
        return HttpResponse("hi")
    init_json = GetJSON(args)
    return HttpResponse(eval('init_json.' + key + '()'))
