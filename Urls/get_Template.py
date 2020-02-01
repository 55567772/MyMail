# coding: utf-8
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin, xframe_options_deny
import datetime
import json
from Codes import MSSQL


@xframe_options_exempt
def redirect(request, page_name):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET
    conn = MSSQL()
    # 检查页面权限
    page_name = str(page_name).strip().replace("'", "")
    sql = "select * from Page_Manager where PageUrl = '{}'".format(page_name)
    res = conn.sDB(sql)
    pur = dict()
    if res:
        LoginInfo  = request.session.get('LoginInfo', {})
        pur = json.loads(LoginInfo['Pur'])
        PageID = res[0]['ID']
        if not (PageID in pur['ID'] or LoginInfo['isSuper']):
            return render(request, '404.html', context={"err": '无权限'})
    else:
        PageID = 0
    print(PageID, pur)
    try:
        return render(request, page_name,
                      context={
                          # 登陆信息
                          "LoginInfo": request.session.get('LoginInfo', ''),
                          # 传入当前用户页面权限
                          "Pur": json.loads(request.session.get('LoginInfo', {})['Pur']),
                          # 传入当前页面对应ID
                          "PageID": PageID,
                          # 传入当时时间
                          "DateTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          # 传入前端的参数
                          "args": args,
                          # 版本号
                          "ver": "20200201",
                      })
    except:
        return render(request, '404.html', context={"err": '404'})
