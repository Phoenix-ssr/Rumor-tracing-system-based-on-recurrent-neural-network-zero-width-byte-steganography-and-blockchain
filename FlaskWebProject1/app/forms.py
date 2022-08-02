# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
#注册表
from wtforms.validators import ValidationError,Email,EqualTo
from app.models import User,Article

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
#注册
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    #校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请您重新换一个呗!')
    #校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复了，请您重新换一个呗!')
class ArticleForm(FlaskForm):
	#title= TextAreaField('标题', validators=[Length(min=0, max=20)])
	#head = TextAreaField('简述', validators=[Length(min=0, max=30)])
	body = TextAreaField('文章', validators=[Length(min=0, max=4000)])
	submit = SubmitField('发布')