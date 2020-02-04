# coding: utf-8
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib import messages
from Codes import MSSQL
import json
from xpinyin import Pinyin
import datetime
import decimal
from Codes import Functions
import time


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


# sql 安全过滤函数
def safe(sql):
    sql = sql.replace("'", "''")
    return sql


# 递归获取管理权限 - 为首页
def loop_pur_for_main(ParentID, auto_list=list, pur=[], isSuper=0):
    """
        参数说明
        ParentID: 父级ID
        menu: 继承的上级dic
    """
    sql = "Select [ID], [PageName] as title, [PageUrl] as href, [PageIcon] as icon " \
          "From Page_Manager where [ParentID] = {0}".format(ParentID)
    res = conn.sDB(sql)
    for row in res:
        row['children'] = loop_pur_for_main(row['ID'], [], pur, isSuper)
        if row['title'] in ['首页', '业务管理']:
            row['isCurrent'] = True
        if row['ID'] in pur['ID'] or row['children'] or isSuper:
            auto_list.append(row)
    return auto_list


# 递归获取管理权限 - 为用户权限分配页
def loop_pur_for_admin(ParentID, auto_list=list, pur={}):
    """
        参数说明
        ParentID: 父级ID
        menu: 继承的上级dic
    """
    sql = "Select [ID], [PageName] as title, [PageUrl] as href, [PageIcon] as icon,ParentID " \
          "From Page_Manager where [ParentID] = {0}".format(ParentID)
    res = conn.sDB(sql)
    for row in res:
        # 修改权
        row['Modify'] = row['ID'] if row['ID'] in pur.get('Modify', []) else 0

        # 修删除
        row['Delete'] = True if row['ID'] in pur.get('Delete', []) else False

        if row['ID'] in pur['ID']:
            row['checked'] = True
        else:
            row['checked'] = False
        row['children'] = loop_pur_for_admin(row['ID'], [], pur)
        auto_list.append(row)
    return auto_list


class GetJSON:
    def __init__(self, request, args=dict):
        self.args = args.copy()
        self.request = request

    # 判断是否为时间格式
    def isDate(self, date):
        try:
            if ":" in date:
                time.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False

    # 查询承运商列表
    def aa(self):
        other_sql = "where 1=1 "
        Carder_MarkName = safe(self.args.get('Carder_MarkName', '')) or safe(self.args.get('q', ''))
        Carder_MarkName = "%s" % safe(Carder_MarkName.strip().replace("'", ""))
        Carder_Type = "%s" % safe(self.args.get('Carder_Type', '').strip().replace("'", ""))
        Carder_BakInfo = "%s" % safe(self.args.get('Carder_BakInfo', '').strip().replace("'", ""))

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
                sql = "INSERT INTO Carder(Carder_MarkName, Carder_Mobile, " \
                      "Carder_Address, Carder_User, Carder_BankUserName, " \
                      "Carder_BankNumber, Carder_BankLive, Carder_Type, " \
                      "Carder_CarNumber, Carder_BakInfo, Carder_CarType, Carder_PY) " \
                      "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')" \
                              .format(safe(self.args.get('Carder_MarkName', '')),
                                      safe(self.args.get('Carder_Mobile', '')),
                                      safe(self.args.get('Carder_Address', '')),
                                      safe(self.args.get('Carder_User', '')),
                                      safe(self.args.get('Carder_BankUserName', '')),
                                      safe(self.args.get('Carder_BankNumber', '')),
                                      safe(self.args.get('Carder_BankLive', '')),
                                      safe(self.args.get('Carder_Type', '')),
                                      safe(self.args.get('Carder_CarNumber', '')),
                                      safe(self.args.get('Carder_BakInfo', '')),
                                      safe(self.args.get('Carder_CarType', '')),
                                      p.get_initials(self.args.get('Carder_MarkName', ''), ''))
                conn.eDB(sql)
                res_id = conn.sDB("select cast(IDENT_CURRENT('Carder') as nvarchar(20)) as ID")[0]
                self.args['ID'] = int(res_id['ID'])
            else:
                sql = "UPDATE Carder Set Carder_MarkName = '{0}', Carder_Mobile = '{1}', " \
                      "Carder_Address = '{2}', Carder_User = '{3}', Carder_BankUserName = '{4}', " \
                      "Carder_BankNumber = '{5}', Carder_BankLive = '{6}', Carder_Type = '{7}', " \
                      "Carder_CarNumber = '{8}', Carder_BakInfo = '{9}', Carder_CarType = '{10}', " \
                      "Carder_PY = '{11}' where ID='{12}'" \
                              .format(safe(self.args.get('Carder_MarkName', '')),
                                      safe(self.args.get('Carder_Mobile', '')),
                                      safe(self.args.get('Carder_Address', '')),
                                      safe(self.args.get('Carder_User', '')),
                                      safe(self.args.get('Carder_BankUserName', '')),
                                      safe(self.args.get('Carder_BankNumber', '')),
                                      safe(self.args.get('Carder_BankLive', '')),
                                      safe(self.args.get('Carder_Type', '')),
                                      safe(self.args.get('Carder_CarNumber', '')),
                                      safe(self.args.get('Carder_BakInfo', '')),
                                      safe(self.args.get('Carder_CarType', '')),
                                      p.get_initials(self.args.get('Carder_MarkName', ''), ''),
                                      safe(self.args.get('ID', '')))
                conn.eDB(sql)
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
        all_result = dict()
        footer = dict()
        other_sql = "where 1=1 "
        Mobile_OrderNumber = "%s" % safe(self.args.get('Mobile_OrderNumber', '').strip().replace("'", ""))
        Carder_ID = "%s" % safe(self.args.get('Carder_ID', '').strip().replace("'", ""))
        Mobile_Client = "%s" % safe(self.args.get('Mobile_Client', '').strip().replace("'", ""))
        Mobile_Bak_Info = "%s" % safe(self.args.get('Mobile_Bak_Info', '').strip().replace("'", ""))
        sTime = self.args.get('sTime', '') if self.isDate(self.args.get('sTime', '')) else ''
        eTime = self.args.get('eTime', '') if self.isDate(self.args.get('eTime', '')) else ''
        month = int(self.args.get('month', 0)) if self.args.get('month', 0) else 0

        if Mobile_OrderNumber:
            other_sql += "and Mobile_OrderNumber like '%{0}%'".format(Mobile_OrderNumber)
        if Carder_ID:
            other_sql += "and Carder_ID = '{0}'".format(Carder_ID)
        if Mobile_Client:
            other_sql += "and Mobile_Client like '%{0}%'".format(Mobile_Client)
        if Mobile_Bak_Info:
            other_sql += "and Mobile_Bak_Info like '%{0}%'".format(Mobile_Bak_Info)
        if sTime:
            other_sql += "and DateDiff(d,'{0}', DateTime)>=0".format(sTime)
        if eTime:
            other_sql += "and DateDiff(d,DateTime,'{0}')>=0".format(eTime)
        if month:
            other_sql += "and month(DateTime)={0} and year(DateTime)=year(GETDATE())".format(month)
        # print(other_sql)

        sql = 'Select *, dbo.Get_CarderMarkName(Carder_ID) as Carder_MarkName from Mobile {0} order by ID desc'.format(other_sql)
        result = conn.sDB(sql)
        # 为footer计算总和，下面罗列需要统计的字段
        fields_total = dict()
        fields = ['Mobile_Goods_Count', 'Mobile_Goods_Square', 'Mobile_KG',
                  'Mobile_CJ_Other_Price', 'Mobile_CJ_Price_Count', 'Mobile_CB_Other_Price', 'Mobile_CB_Price_Count']
        for row in result:
            for f in fields:
                fields_total[f] = fields_total.get(f, 0) + row[f]
        # print(fields_total)
        # 脚部数据
        for k, v in fields_total.items():
            footer[k] = v
        footer['DateTime'] = "统计"
        # 组合所有数据
        all_result['total'] = len(result)
        all_result['rows'] = result
        all_result['footer'] = [footer]
        return str(json.dumps(all_result, cls=DateEncoder))

    # 添加，修改 订单
    def ae(self):
        Mobile_OrderNumber = "TC" + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        DateTime = self.args.get('DateTime', datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        # 根据Carder_ID取承运商名字
        Carder_ID = self.args.get('Carder_ID', 0)
        sql_1 = "select dbo.Get_CarderMarkName('{0}') as Carder_MarkName".format(Carder_ID)
        self.args['Carder_MarkName'] = conn.sDB(sql_1)[0]['Carder_MarkName']
        try:
            if self.args['EditType'] == 'add':
                sql = "INSERT INTO Mobile(" \
                     "Mobile_OrderNumber, Carder_ID, Mobile_Client, " \
                     "Mobile_Goods, Mobile_Goods_Count, Mobile_Goods_Square, " \
                     "Mobile_KG, Mobile_Receive_Person, Mobile_Contact_Type, " \
                     "Mobile_Address, Mobile_Start_Address, Mobile_End_Address, " \
                     "Mobile_CJ_Price, Mobile_CJ_Other_Price, Mobile_CJ_Price_Count, " \
                     "Mobile_CB_Price, Mobile_CB_Other_Price, Mobile_CB_Price_Count, " \
                     "Mobile_Clear_Type, Mobile_Make_Tick, DateTime,AdminInfo, Mobile_Bak_Info) values " \
                     "('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}'," \
                     "'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}')" \
                     .format(Mobile_OrderNumber,
                             Carder_ID,
                             safe(self.args.get('Mobile_Client', '')),
                             safe(self.args.get('Mobile_Goods', '')),
                             float(self.args.get('Mobile_Goods_Count', 0)),
                             float(self.args.get('Mobile_Goods_Square', 0)),
                             float(self.args.get('Mobile_KG', 0)),
                             safe(self.args.get('Mobile_Receive_Person', '')),
                             safe(self.args.get('Mobile_Contact_Type', '')),
                             safe(self.args.get('Mobile_Address', '')),
                             safe(self.args.get('Mobile_Start_Address', '')),
                             safe(self.args.get('Mobile_End_Address', '')),
                             float(self.args.get('Mobile_CJ_Price', 0)),
                             float(self.args.get('Mobile_CJ_Other_Price', 0)),
                             float(self.args.get('Mobile_CJ_Price_Count', 0)),
                             float(self.args.get('Mobile_CB_Price', 0)),
                             float(self.args.get('Mobile_CB_Other_Price', 0)),
                             float(self.args.get('Mobile_CB_Price_Count', 0)),
                             safe(self.args.get('Mobile_Clear_Type', '')),
                             safe(self.args.get('Mobile_Make_Tick', '')),
                             DateTime,
                             '[' + self.request.session['LoginInfo']['NickName'] +
                             '] 新增于:' + datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
                             safe(self.args.get('Mobile_Bak_Info', '')))
                print(sql)
                conn.eDB(sql)
                res_id = conn.sDB("select cast(IDENT_CURRENT('Carder') as nvarchar(20)) as ID")[0]
                self.args['ID'] = int(res_id['ID'])
                self.args['Mobile_OrderNumber'] = Mobile_OrderNumber
                return str(json.dumps({"err": False, "data": self.args}))
            else:
                sql = "update Mobile set Carder_ID='{0}', Mobile_Client='{1}', " \
                      "Mobile_Goods='{2}', Mobile_Goods_Count='{3}', Mobile_Goods_Square='{4}', " \
                      "Mobile_KG='{5}', Mobile_Receive_Person='{6}', Mobile_Contact_Type='{7}', " \
                      "Mobile_Address='{8}', Mobile_Start_Address='{9}', Mobile_End_Address='{10}', " \
                      "Mobile_CJ_Price='{11}', Mobile_CJ_Other_Price='{12}', Mobile_CJ_Price_Count='{13}', " \
                      "Mobile_CB_Price='{14}',Mobile_CB_Other_Price='{15}', Mobile_CB_Price_Count='{16}', " \
                      "Mobile_Clear_Type='{17}', Mobile_Make_Tick='{18}', AdminInfo=AdminInfo + '{19}', " \
                      "Mobile_Bak_Info='{20}',Mobile_isModify=1 where ID='{21}'"\
                    .format(Carder_ID,
                            safe(self.args.get('Mobile_Client', '')),
                            safe(self.args.get('Mobile_Goods', '')),
                            float(self.args.get('Mobile_Goods_Count', 0)),
                            float(self.args.get('Mobile_Goods_Square', 0)),
                            float(self.args.get('Mobile_KG', 0)),
                            safe(self.args.get('Mobile_Receive_Person', '')),
                            safe(self.args.get('Mobile_Contact_Type', '')),
                            safe(self.args.get('Mobile_Address', '')),
                            safe(self.args.get('Mobile_Start_Address', '')),
                            safe(self.args.get('Mobile_End_Address', '')),
                            float(self.args.get('Mobile_CJ_Price', 0)),
                            float(self.args.get('Mobile_CJ_Other_Price', 0)),
                            float(self.args.get('Mobile_CJ_Price_Count', 0)),
                            float(self.args.get('Mobile_CB_Price', 0)),
                            float(self.args.get('Mobile_CB_Other_Price', 0)),
                            float(self.args.get('Mobile_CB_Price_Count', 0)),
                            safe(self.args.get('Mobile_Clear_Type', '')),
                            safe(self.args.get('Mobile_Make_Tick', '')),
                            '<br>[' + self.request.session['LoginInfo']['NickName'] +
                            '] 编辑于:' + datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
                            safe(self.args.get('Mobile_Bak_Info', '')),
                            int(self.args.get('ID', 0)))
                conn.eDB(sql)
                return str(json.dumps({"err": False, "data": self.args}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 删除订单
    @csrf_exempt
    def af(self):
        try:
            conn.eDB("DELETE FROM Mobile WHERE ID = '{0}'".format(int(self.args.get('ID', 0))))
            return str(json.dumps({"err": False, "data": "ok"}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 首页的一些统计
    def ag(self):
        main_dict = dict()
        main_count = dict()
        # 统计承运商数量
        res = conn.sDB("select count(ID) as c from Carder")
        main_count['carder_count'] = res[0]['c']
        # 统计未录入承运商的订单
        res = conn.sDB("select count(ID) as c from Mobile where Carder_ID = 0")
        main_count['mobile_carder_null'] = res[0]['c']
        # 统计订单数量、客户数量
        res = conn.sDB("select count(ID) as Mobile_Count, count(distinct Mobile_Client) as Mobile_Client_Count "
                       "from Mobile where year(DateTime)=YEAR(GETDATE())")[0]
        main_count = dict(main_count, **res)
        # 压入顶部字典
        main_dict['main_count'] = main_count
        # 承运商订单数量比例图表数据
        option0 = conn.sDB("select count(ID) as value,dbo.Get_CarderMarkName(Carder_ID) as name from Mobile where Carder_ID<>0 group by Carder_ID")
        main_dict['option0'] = option0
        # 按周计算订单数量
        sql = "select count(ID) as c,'第'+ datename(week,DateTime) +'周' as week " \
              "from Mobile where DateDiff(week,DateTime,GETDATE())<=7 group by DateName(week,DateTime)"
        res = conn.sDB(sql)
        option1 = {}; option1['week'] = []; option1['data'] = []
        for row in res:
            print(row)
            option1['week'].append(row['week'])
            option1['data'].append(row['c'])
        main_dict['option1'] = option1
        # main_dict['option1'] = 1
        # print(list_week,list_data)
        return HttpResponse(json.dumps(main_dict))

        # Car = "select count(ID) from Mobile where year(DateTime)=YEAR(GETDATE())"


    # 获取页面权限树
    @csrf_exempt
    def sa(self):
        all_element = list()
        pur = json.loads(self.request.session['LoginInfo']['Pur'])
        isSuper = self.request.session['LoginInfo']['isSuper']
        all_element.extend(loop_pur_for_main(0, [], pur, isSuper))
        # # try:
        # sql = "Select [ID], [PageName] as title, [PageUrl] as href, [PageIcon] as icon " \
        #       "From Page_Manager where [ParentID] = 0"
        # res = conn.sDB(sql)
        # for row in res:
        #     if row['title'] in ['首页', '业务管理']:
        #         row['isCurrent'] = True
        #     row['children'] = loop_pur_for_main(row['ID'], [], pur, isSuper)
        #     if row['ID'] in pur['ID'] or row['children'] or isSuper:
        #         all_element.append(row)
        return "var SystemMenu = " + json.dumps(all_element)

    # 保存用户页面权限
    @csrf_exempt
    def sb(self):

        try:
            pur_json = json.loads(self.args['Pur'])
            tmp_dict = dict()
            # 储存页面ID
            tmp_dict['ID'] = []
            # 储存页面地址
            tmp_dict['href'] = []
            # 储存修改权限
            tmp_dict['Modify'] = []
            for row in pur_json:
                tmp_dict['ID'].append(row['ID'])
                tmp_dict['href'].append(row['href'])
                tmp_dict['Modify'].append(row['Modify'])
            sql = "update Admin set Pur = '{0}' where ID = {1}".format(json.dumps(tmp_dict), int(self.args['ID']))
            print(sql)
            conn.eDB(sql)
            return HttpResponse(json.dumps({"err": False, "msg": "成功保存1"}))
        except Exception as err:
            return HttpResponse(json.dumps({"err": True, "msg": str(err)}))

    # 查询管理员
    def ua(self):
        other_sql = "where 1=1 "
        NickName = "%s" % safe(self.args.get('NickName', '').strip())
        # NickName = "%s" % self.args.get('NickName', '').strip().replace("'", "")

        if NickName:
            other_sql += "and NickName like '%{0}%'".format(NickName)

        sql = 'Select * from Admin {0}'.format(other_sql)
        result = conn.sDB(sql)
        return str(json.dumps(result, cls=DateEncoder))

    # 添加，修改 管理员
    def ub(self):
        try:
            if self.args['EditType'] == 'add':
                sql = "INSERT INTO Admin(u, p, NickName, InGroup) "\
                         "values ('{0}','{1}','{2}','{3}')"\
                         .format(safe(self.args.get('u', '')),
                                 safe(self.args.get('p', '')),
                                 safe(self.args.get('NickName', '')),
                                 safe(self.args.get('InGroup', '')))
                conn.eDB(sql)
                res_id = conn.sDB("select cast(IDENT_CURRENT('Admin') as nvarchar(20)) as ID")[0]
                self.args['ID'] = int(res_id['ID'])
            else:
                sql = "UPDATE Admin Set "\
                         "p = '{0}', "\
                         "NickName = '{1}', "\
                         "InGroup = '{2}' "\
                         "where ID='{3}'"\
                         .format(safe(self.args.get('p', '')),
                                 safe(self.args.get('NickName', '')),
                                 safe(self.args.get('InGroup', '')),
                                 int(self.args.get('ID', '')))
                conn.eDB(sql)
            return str(json.dumps({"err": False, "data": self.args}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 删除用户
    @csrf_exempt
    def uc(self):
        try:
            conn.eDB("DELETE FROM Admin WHERE isSuper<>1 and ID = '{0}'".format(int(self.args['ID'])))
            return str(json.dumps({"err": False, "data": "ok"}))
        except Exception as err:
            return str(json.dumps({"err": str(err)}))

    # 权限树 用户权限分配页面
    @csrf_exempt
    def pa(self):
        try:
            ID = int(self.args.get('ID', 0))
            res = conn.sDB("select * from Admin where ID = {0}".format(ID))[0]
            pur = json.loads(res['Pur'])
            all_element = list()
            all_element.extend(loop_pur_for_admin(0, [], pur))
            return json.dumps(all_element)
        except Exception as err:
            return json.dumps({"err": True, "msg": str(err)})

    # 修改用户密码
    @csrf_exempt
    def pb(self):
        if self.request.session.get('LoginInfo', ''):
            try:
                p = safe(self.args.get('p', '').strip())
                u = self.request.session['LoginInfo']['u']
                sql = "update Admin set p='{0}' where u='{1}'".format(p, u)
                # print(sql)
                conn.eDB(sql)
                return json.dumps({"err": False, "msg": "ok"})
            except Exception as err:
                return json.dumps({"err": True, "msg": str(err)})
        else:
            return json.dumps({"err": True, "msg": "无权限"})

    # 安全退出
    @csrf_exempt
    def pc(self):
        if self.request.session.get('LoginInfo', ''):
            del self.request.session['LoginInfo']
            return json.dumps({"err": False, "msg": "已退出1"})
        else:
            return json.dumps({"err": False, "msg": "已退出2"})

    # 登陆验证
    def lo(self):
        u = self.request.POST.get('u', '').replace("'", "''")
        p = self.request.POST.get('p', '').replace("'", "''")
        # sql = "select * from Admin where UserName='{0}' and PassWord='{1}'"\
        #     .format(username, password)
        sql = "Select u,NickName,Pur,isSuper from Admin where [u] = '{0}' and [p] = '{1}'".format(u, p)
        res = conn.sDB(sql)
        if res:
            self.request.session['LoginInfo'] = res[0]
            # # 权限项是列表，取出来格式化再传入
            # self.request.session['LoginInfo']['Pur'] = json.loads(res[0]['Pur'])
            # self.request.session['Pur'] = res['Pur']
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
