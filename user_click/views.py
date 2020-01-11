from django.shortcuts import render
import matplotlib.pyplot as plt
from db_pro import settings
import pymysql
import random
from django.http import *
from user_click.models import *

# Create your views here.

index_img = 1
from pyhanlp import *

def index(request):
    HanLP.Config.enableDebug()


    print(HanLP.segment("王国维和服务员"))

    return render(request, 'index.html')


def process(request):
    HanLP.Config.enableDebug()
    str_1 = request.POST.get("str_process")
    if str_1 is None:
        str_1 = '你好世界'

    print(HanLP.segment(str_1))
    pro_res=HanLP.segment(str_1)

    print(str_1)
    return render(request, 'index.html',locals())


def upload(request):
    a = request.POST
    print(a)
    import base64
    img = base64.b64decode(a['img'])

    global index_img
    path = settings.IMG_ROOT +str(index_img) + "out"+'.jpg'
    with open(path, 'wb') as f:
        f.write(img) # 保存图片完成

    Rotate.runmain()

    index_img = index_img + 1
    print(id(index_img))
    print(index_img)
    from aip import AipOcr
    import re
    APP_ID = '17964129'
    API_KEY = 'GlalvqRlGVrIH67fv2uxLBoT'
    SECRECT_KEY = 'Mzt1SZj20PozVY0o7fXXiF82P0E2HaBZ'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    i = open(path, 'rb')
    img = i.read()
    message = client.basicGeneral(img)
    print(message)
    # for i in message.get('words_result'):
    #     print(i.get('words'))
    words = message['words_result']
    messaget=' '

    for i in range(0,len(words)):
        messaget=messaget+words[i]['words']
    conn = pymysql.connect("localhost", "root", "123456", "database_pro")
    cur = conn.cursor()
    if a is None:
        a = ''

    sql = '''insert into problem(type,userNo,problem_des) VALUES("DP","1"," ''' + messaget +  '")'
    print(sql)

    cur.execute(sql)


    conn.commit()
    cur.close()
    conn.close()
    return JsonResponse({"words":words})


