# coding: utf-8
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from Codes import MSSQL
import json
from xpinyin import Pinyin
from django.shortcuts import redirect
import datetime
import decimal
from Codes import Functions


conn = MSSQL()


class DateEncoder(json.JSONEncoder):
    """ 用于解决 JSON 无法序列化 DateTime格式的类 """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        if isinstance(obj, decimal.Decimal):
            return float(obj)

        else:
            return json.JSONEncoder.default(self, obj)

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
    def __init__(self, request, args=dict):
        self.args = args.copy()
        self.request = request

    # 查询承运商列表
    def aa(self):
        other_sql = "where 1=1 "
        Carder_MarkName = self.args.get('Carder_MarkName', '') or self.args.get('q', '')
        Carder_MarkName = "%s" % Carder_MarkName.strip().replace("'", "")
        Carder_Type = "%s" % self.args.get('Carder_Type', '').strip().replace("'", "")
        Carder_BakInfo = "%s" % self.args.get('Carder_BakInfo', '').strip().replace("'", "")

        if Carder_MarkName:
            other_sql += "and Carder_MarkName like '%{0}%'".format(Carder_MarkName)
        if Carder_Type:
            other_sql += "and Carder_Type = '{0}'".format(Carder_Type)
        if Carder_BakInfo:
            other_sql += "and Carder_BakInfo like '%{0}%'".format(Carder_BakInfo)
        sql = 'Select * from Carder {0} order by ID desc'.format(other_sql)
        result = conn.sDB(sql)
        return str(json.dumps(result, cls=DateEncoder))

    # 添加，修改 承运商
    def ab(self):
        try:
            # 拼音
            p = Pinyin()
            if self.args['EditType'] == 'add':
                conn.eDB("INSERT INTO Carder(Carder_MarkName, Carder_Mobile, "
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
                res_id = conn.sDB("select cast(IDENT_CURRENT('Carder') as nvarchar(20)) as ID")[0]
                self.args['ID'] = int(res_id['ID'])
            else:
                conn.eDB("UPDATE Carder Set Carder_MarkName = '{0}', Carder_Mobile = '{1}', "
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
            conn.eDB("DELETE FROM Carder WHERE ID = '{0}'".format(int(self.args['ID'])))
            return str(json.dumps({"err": False, "data": "ok"}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 查询订单
    def ad(self):

        other_sql = "where 1=1 "
        Mobile_OrderNumber = "%s" % self.args.get('Mobile_OrderNumber', '').strip().replace("'", "")
        Carder_ID = "%s" % self.args.get('Carder_ID', '').strip().replace("'", "")
        Mobile_Client = "%s" % self.args.get('Mobile_Client', '').strip().replace("'", "")

        if Mobile_OrderNumber:
            other_sql += "and Mobile_OrderNumber like '%{0}%'".format(Mobile_OrderNumber)
        if Carder_ID:
            other_sql += "and Carder_ID = '{0}'".format(Carder_ID)
        if Mobile_Client:
            other_sql += "and Mobile_Client like '%{0}%'".format(Mobile_Client)
        sql = 'Select *,' \
              '(select top 1 Carder_MarkName from Carder where ID = [Mobile].Carder_ID) as Carder_MarkName ' \
              'from Mobile {0} order by ID desc'.format(other_sql)
        result = conn.sDB(sql)
        return str(json.dumps(result, cls=DateEncoder))

    # 添加，修改 订单
    def ae(self):
        Mobile_OrderNumber = "TC" + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        try:
            conn.eDB("INSERT INTO Mobile("
                     "Mobile_OrderNumber, Carder_ID, Mobile_Client, "
                     "Mobile_Goods, Mobile_Goods_Count, Mobile_Goods_Square, "
                     "Mobile_KG, Mobile_Receive_Person, Mobile_Contact_Type, "
                     "Mobile_Address, Mobile_CJ_Price, Mobile_CJ_Price_Count, "
                     "Mobile_CB_Price, Mobile_CB_Price_Count, Mobile_Clear_Type, Mobile_Make_Tick) values "
                     "('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',"
                     "'{10}','{11}','{12}','{13}','{14}','{15}')"
                     .format(Mobile_OrderNumber,
                             self.args.get('Carder_ID', ''),
                             self.args.get('Mobile_Client', ''),
                             self.args.get('Mobile_Goods', ''),
                             self.args.get('Mobile_Goods_Count', ''),
                             self.args.get('Mobile_Goods_Square', ''),
                             self.args.get('Mobile_KG', ''),
                             self.args.get('Mobile_Receive_Person', ''),
                             self.args.get('Mobile_Contact_Type', ''),
                             self.args.get('Mobile_Address', ''),
                             self.args.get('Mobile_CJ_Price', ''),
                             self.args.get('Mobile_CJ_Price_Count', ''),
                             self.args.get('Mobile_CB_Price', ''),
                             self.args.get('Mobile_CB_Price_Count', ''),
                             self.args.get('Mobile_Clear_Type', ''),
                             self.args.get('Mobile_Make_Tick', ''))
                     )
            res_id = conn.sDB("select cast(IDENT_CURRENT('Carder') as nvarchar(20)) as ID")[0]
            self.args['ID'] = int(res_id['ID'])
            self.args['Mobile_OrderNumber'] = Mobile_OrderNumber
            return str(json.dumps({"err": False, "data": self.args}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 删除订单
    @csrf_exempt
    def af(self):
        try:
            conn.eDB("DELETE FROM Mobile WHERE ID = '{0}'".format(int(self.args['ID'])))
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

    # 登陆验证
    def lo(self):
        u = self.request.POST.get('u', '').replace("'", "''")
        p = self.request.POST.get('p', '').replace("'", "''")
        # sql = "select * from Admin where UserName='{0}' and PassWord='{1}'"\
        #     .format(username, password)
        sql = "Select u,NickName,Pur from Admin where [u] = '{0}' and [p] = '{1}'".format(u, p)
        res = conn.sDB(sql)
        if res:
            self.request.session['LoginInfo'] = res[0]
            # self.request.session['username'] = username
            conn.eDB("update Admin set LoginTime = GETDATE() where u = '{0}'".format(u))
            return JsonResponse({"err": False, "url": '/get_tpl/main.html'})
        else:
            return JsonResponse({"err": True})


@csrf_protect
def redirect(request, key):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET
    if not key:
        return HttpResponse("hi")
    init_json = GetJSON(request, args)
    return HttpResponse(eval('init_json.' + key + '()'))
