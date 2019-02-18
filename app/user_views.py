import os
import random
import re
import uuid

from flask import Blueprint, request
from flask import render_template, redirect, jsonify, session
from flask_login import login_user, LoginManager, login_required, logout_user
from werkzeug.security import check_password_hash

from app.models import User

user_blue = Blueprint('user', __name__)
login_manage = LoginManager()


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1000, 'msg': '有参数未填写'})
    # 2. 验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1001, 'msg': '手机号不正确'})
    # 3. 验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1002, 'msg': '验证码不正确'})
    # 4. 密码是否一致
    if passwd2 != passwd:
        return jsonify({'code': 1003, 'msg': '密码不一致'})

    # 5手机号是否被注册
    user = User.query.filter(User.phone == mobile).first()
    if user:
        return jsonify({'code': 1004, 'msg': '手机号已经被注册'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': 'success'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码地址
    # 方式2：后端值生成随机参数，返回给页面，在页面生成图片(前段做)
    str = '123456789qwertyuiopashdjklzxcvbbnm'
    code = ''
    for i in range(6):
        code += random.choice(str)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 登录
@user_blue.route('/login/', methods=['POST'])
def my_login():
    # 获取数据
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    # 判断是否用户是否存在
    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code': 1001, 'msg': '用户未注册'})
    # 判断密码是否正确
    if not check_password_hash(user.pwd_hash, passwd):
        return jsonify({'code': 1002, 'msg': '密码错误'})
    login_user(user)
    return jsonify({'code': 200, 'msg': 'success'})


@login_manage.user_loader
def load_user(user_id):
    # 定义被login_manage装饰的回调函数
    # 返回的是当前登录系统的用户对象
    return User.query.filter(User.id == user_id).first()


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


# 个人信息
@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    user = User.query.filter_by(id=session['user_id']).first()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/profile/', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


# 修改个人信息页面
@user_blue.route('/profile/', methods=['PATCH'])
@login_required
def my_profile():
    # 获取数据
    avatar = request.files.get('avatar')
    name = request.form.get('name')
    if avatar:
        # 拼接路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        MIDIA_DIR = os.path.join(STATIC_DIR, 'media')
        filename = str(uuid.uuid4())
        a = avatar.mimetype.split('/')[-1:][0]
        imgname = filename + '.' + a
        path = os.path.join(MIDIA_DIR, imgname)

        # 向media里面保存图片
        avatar.save(path)

        # 获取用户
        user = User.query.filter_by(id=session['user_id']).first()

        # 向数据库保存数据
        user.avatar = '/static' + '/media/' + imgname
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功', 'data': {'avatar': path}})
    if name:
        user = User.query.filter_by(id=session['user_id']).first()

        # 向数据库保存数据
        user.name = name
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功', 'data': {'name': name}})
    return jsonify({'code': 200, 'msg': '未填写数据'})


# 实名认证
@user_blue.route('/auth/', methods=['GET'])
@login_required
def auth():
    return render_template('auth.html')


@user_blue.route('/auth_info/', methods=['GET'])
@login_required
def auth_info():
    user = User.query.filter_by(id=session['user_id']).first()
    if user.id_name:
        return jsonify({'code': 1011, 'msg': '不可编辑', 'data': user.to_auth_dict()})
    return jsonify({'code': 200, 'msg': '请求成功！', 'data': user.to_auth_dict()})


@user_blue.route('/auth/', methods=['POST'])
@login_required
def my_auth():
    real_name = request.form.get('iname')
    id_card = request.form.get('icard')
    if not all([real_name, id_card]):
        return jsonify({'code': 1007, 'msg': '请填写完整信息'})
    if not re.match('^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                    id_card):
        return jsonify({'code': 1008, 'msg': '身份证信息有误，请重新确认'})
    if User.query.filter_by(id_card=id_card).first():
        return jsonify({'code': 1009, 'msg': '身份信息重复'})
    user = User.query.filter_by(id=session['user_id']).first()
    user.id_name = real_name
    user.id_card = id_card
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功！'})


# 退出登录
@user_blue.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'code': 200, 'msg': '退出成功！'})
