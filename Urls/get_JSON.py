# coding: utf-8
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect
from Codes import db
import json
# from xpinyin import Pinyin


class GetJSON:
    def __init__(self, args=dict):
        self.args = args
        self.db = db()

    # 查询承运商列表
    def aa(self):
        sql = "where 1=1 "
        Carder_MarkName = "%s" % self.args.get('Carder_MarkName', '').strip().replace("'", "")
        if Carder_MarkName:
            sql += "and Carder_MarkName like '%{0}%'".format(Carder_MarkName)
        print(sql)
        self.db.execute('Select * from Carder {0}'.format(sql))
        result = self.db.fetchall()
        return str(json.dumps(result))

    # 添加承运商列
    def ab(self):
        self.db.execute('Select * from Carder')
        result = self.db.fetchall()
        # print(result)
        result = {"total": len(result), "rows": result}
        return str(json.dumps(result))


@csrf_protect
def redirect(request, key):
    args = request.POST
    if not key:
        return HttpResponse("hi")
    init_json = GetJSON(args)
    return HttpResponse(eval('init_json.' + key + '()'))
