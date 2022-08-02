'''
Descripttion: 
version: 
Author: A1ertx5s
Date: 2022-03-31 21:32:58
LastEditors: sA1ertx5s
LastEditTime: 2022-06-01 15:52:58
'''
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import re
import json
import pymysql
import requests

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        if "tree" in segment:
            ids = query_db("select rumorid from atricle group by rumorid;")
            return render_template("home/tree.html", segment=segment, ids = ids)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/tree')
@login_required
def tree():

    segment = get_segment(request)

    ids = query_db("select rumorid from article group by rumorid;")
    ids = [id['rumorid'] for id in ids]
    return render_template("home/tree.html", segment=segment, ids = ids)

@blueprint.route('/viewdata/<id>')
@login_required
def viewdata(id):
    # with open('./data/test.json','r',encoding='utf8')as fp:
    #     json_data = json.load(fp)
    # return json_data
    res = requests.get('http://101.35.105.81:3001/get2?id=' + str(id))
    mes = get_hidemassage(res.text)
    id_username = query_db("select id, username from user")
    print(id_username)
    list = []
    for t in mes:
        if t[0] != '0':
            a = [d['username'] for d in id_username if str(d['id']) == t[0]][0]
        else:
            a = '0'
        b = [d['username'] for d in id_username if str(d['id']) == t[1]][0]
        list.append((a, b, 1))

    return jsonify(get_tree(list))


@blueprint.route('/api/rumor-all', methods=["GET", "POST"])
@login_required
def rumor_all():
    if request.method == "GET":
        query = "select a.id, a.rumorid, u.username, from_unixtime(convert(time, SIGNED),'%%Y-%%m-%%d %%H:%%i:%%s') as time, longbody, ifrumor from article as a, user as u where ifrumor_RNN=1 and a.user_id = u.id and a.ifrumor=0;"
        res = query_db(query)
        # print(res)
        return json.dumps(res)
    elif request.method == "POST":
        rumorid = request.form.get('rumorid')
        ifrumor = request.form.get('ifrumor')
        if ifrumor == 'true':
            query_1 = "update article set ifrumor=1 where rumorid = %s"
            query_db(query_1, [rumorid])
        elif ifrumor == 'false':
            query_1 = "update article set ifrumor=-1 where rumorid = %s"
            query_db(query_1, [rumorid])
        return "success"

@blueprint.route('/api/rumor-today', methods=["GET", "POST"])
@login_required
def rumor_today():
    if request.method == "GET":
        query = "select a.id, a.rumorid, u.username, from_unixtime(convert(time, SIGNED),'%%Y-%%m-%%d %%H:%%i:%%s') as time, longbody from article as a, user as u where ifrumor_RNN=1 and a.user_id = u.id and to_days(time)=to_days(now());"
        res = query_db(query)
        return json.dumps(res)
    elif request.method == "POST":
        rumorid = request.form.get('rumorid')
        ifrumor = request.form.get('ifrumor')
        if ifrumor == 'true':
            query_1 = "update article set ifrumor=1 where rumorid = %s"
            query_db(query_1, [rumorid])
        elif ifrumor == 'false':
            query_1 = "update article set ifrumor=-1 where rumorid = %s"
            query_db(query_1, [rumorid])
        return "success"

@blueprint.route('/api/rumor-is', methods=["GET", "POST"])
@login_required
def rumor_is():
    query = "select a.id, a.rumorid, u.username, from_unixtime(convert(time, SIGNED),'%%Y-%%m-%%d %%H:%%i:%%s') as time, longbody from article as a, user as u where ifrumor=1 and a.user_id = u.id;"
    res = query_db(query)
    print(res)
    return json.dumps(res)

@blueprint.route('/api/rumor-not', methods=["GET", "POST"])
@login_required
def rumor_not():
    query = "select a.id, a.rumorid, u.username, from_unixtime(convert(time, SIGNED),'%%Y-%%m-%%d %%H:%%i:%%s') as time, longbody from article as a, user as u where ifrumor=-1 and a.user_id = u.id;"
    res = query_db(query)
    print(res)
    return json.dumps(res)

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None

def get_db():
    # 建立链接
    conn=pymysql.connect(
        host='101.35.105.81',
        port=3000,
        user='root',
        password='123456',
        db='weibo',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
 
    # 拿到游标
    cursor=conn.cursor()
    return conn, cursor

def query_db(query, args=[], one=False):
    conn, cursor = get_db()
    cursor.execute(query, args)
    conn.commit()
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def get_hidemassage(data):
    res = []
    list = data.split('==>')[:-1]
    for l in list:
        #提取to
        toid = re.findall(r'to.*?c',l)[0]
        toid = toid[2:-1]
        #提取from
        fromid = re.findall(r'from.*?to',l)[0]
        fromid = fromid[4:-2]
        res.append((fromid, toid, 1))
    return res

def get_tree(list):
    flag = False
    tuple = list[0][1]
    for t in list:
        if t[0] == tuple:
            flag = True
    if flag:
        return {
            "name": list[0][1],
            "children":[get_tree(list[i:]) for i in range(1,len(list)) if list[i][0] == list[0][1]]
        }
    else:
        return {
            "name": list[0][1], "value":list[0][2]
        }
