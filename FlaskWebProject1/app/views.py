"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,render_template_string
from flask_login import login_required,current_user,login_user,logout_user

from flask import render_template,flash,redirect,url_for,request
from werkzeug.urls import url_parse
from app import app,db
from app.forms import LoginForm,RegistrationForm,ArticleForm
from flask_login import login_required,current_user,login_user,logout_user
from app.models import User,Article
import time,requests

from flask import Markup
#算法主体调用rnn，0z
@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@app.route('/article',methods=['GET','POST'])
@login_required
def article():
    form=ArticleForm()
    t=time.strftime('%Y.%m.%d.%A.%H:%M:%S',time.localtime(time.time()))
    t = time.time()
    if form.validate_on_submit():
        data = form.body.data
        forecast = 0
        ifrumor_RNN = 0
        #检测是否隐写 例子：id0from0to0c000000
        #未隐写进行进行谣言检测嵌入
        #隐写则调整传播次数 和 增加传播路径
        if_zw = zw.check_message(data)
        print(if_zw)
        if if_zw == 1:
            print("已经嵌入信息")
            #已经嵌入信息 隐写则调整传播次数 需要传入当前用户id
            #考虑传播者是否上链
            data,rumorid = zw.change_message(data,str(current_user.id))#需要返回谣言id
            ifrumor_RNN = 1
            #上链
            data2 = zw.nonezero_2_string(data);
            url = "http://127.0.0.1:3000/add"
            param = {'id':rumorid,'message':data}
            response = requests.get(url,params=param)
            url = "http://127.0.0.1:3000/add2"
            param = {'id':rumorid,'message':data2}
            response = requests.get(url,params=param)
        elif if_zw == 0:#初始化上链
            Forecast = RNN.forecast(form.body.data)
            #读取谣言的序号
            with open(r"./rumorid.txt") as f:
                rumorid = f.readline()
                rumorid = int(rumorid)
            with open('rumorid.txt','w',encoding='utf-8') as f:
                f.write(str(rumorid+1))
            if(Forecast["预测结果标签"]==0):
                #算法断定是谣言,嵌入信息
                print("谣言")
                ifrumor_RNN = 1
                forecast = int(str(int(float(Forecast["概率"])*1000)).ljust(4,'0'))
                #data = zw.hide_message(form.body.data,str(current_user.id)+"000000")
                data2 = "id"+str(rumorid)+"from"+"0"+"to"+str(current_user.id)+"c000000"
                data = zw.hide_message(form.body.data,data2)
            #上链
                url = "http://127.0.0.1:3000/add"
                param = {'id':rumorid,'message':data}
                response = requests.get(url,params=param)
                url = "http://127.0.0.1:3000/add2"
                param = {'id':rumorid,'message':data2}
                response = requests.get(url,params=param)
            else:
                print("非谣言")
                article = Article(longbody=data,author=current_user,time=t,forecast=forecast,ifrumor=0,ifrumor_RNN=ifrumor_RNN,rumorid=rumorid)
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('article'))
        print("flash")  
        article = Article(longbody=data,author=current_user,time=t,forecast=forecast,ifrumor=0,ifrumor_RNN=ifrumor_RNN,rumorid=rumorid)
        db.session.add(article)
        db.session.commit()
        flash('你已经成功发文.')
        return redirect(url_for('article'))
    article = Article.query.all()
    article = article[::-1]
    return render_template('article.html',form=form,articles=article)
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('article'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('article')
        return redirect(next_page) 
    return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    #if current_user.is_authenticated:
    #    return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)