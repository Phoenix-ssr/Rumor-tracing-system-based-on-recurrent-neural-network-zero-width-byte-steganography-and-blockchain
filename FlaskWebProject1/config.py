import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = 'adqwfdfa!@$$#@$%%adfe#@$'
    #.......
    #格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/weibo?charset=utf8'
    #如果你不打算使用mysql，使用这个连接sqlite也可以
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
