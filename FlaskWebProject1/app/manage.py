from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
#from . import app,db,migrate
# 在进行迁移时,必须导入模型,不然数据库不会改变
from .models import Article,User


manager = Manager(app)

# 2.把migrateCommand命令添加到manager中。
manager.add_command('db', MigrateCommand)


if __name__ == '__name__':
    manager.run()