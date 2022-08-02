
#-*- encoding:utf-8 -*-
from flask_login import UserMixin
from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
#用户 #未提供好友模式，对所有的文章进行打印
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article',backref='author',lazy='dynamic')
    
    def __repr__(self):
        return '<用户名：{}>'.format(self.id)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#发文
class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer,primary_key=True)
    #文本内容
    longbody = db.Column(db.String(4000))
    #研判
    ifrumor_RNN = db.Column(db.Integer)
    ifrumor = db.Column(db.Integer)
    #预测结果（概率）
    forecast = db.Column(db.Integer)
    time=db.Column(db.Integer)
    #本系统谣言排序
    rumorid = db.Column(db.Integer)
    #绑定用户信息，通过用户id绑定
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self): return '{}'.format(self.id)
   
class Post(db.Model):
    __tablename__ = 'post'
    #评论id
    id = db.Column(db.Integer,primary_key=True)
    #评论内容
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    #发送用户
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #接收用户
    user_to_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #回复哪一条评论
    reply_id = db.Column(db.Integer,index=True)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))