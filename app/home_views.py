import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, session, request
from flask_login import login_required
from sqlalchemy import and_

from app.models import User, Area, Facility, House, HouseImage, Order

home_blue = Blueprint('home', __name__)


# 我的房源页面
@home_blue.route('/myhouse/', methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')


# 判断是否实名认证
@home_blue.route('/is_auth/', methods=['GET'])
@login_required
def is_auth():
    user = User.query.filter_by(id=session['user_id']).first()
    if not all([user.id_name, user.id_card]):
        return jsonify({'code': 1010, 'msg': '未实名认证'})
    return jsonify({'code': 200, 'msg': '已经实名认证'})


# 我的房源页面传递房源房源信息
@home_blue.route('/myhouse_info/', methods=['GET'])
@login_required
def myhouse_info():
    houses = House.query.filter_by(user_id=session['user_id']).all()
    all_house = []
    for i in range(len(houses)):
        all_house.append(houses[i].to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data': all_house})


# 发布房源页面传递城区
@home_blue.route('/house_info/', methods=['GET'])
def house_info():
    area_list = Area.query.all()
    # 组装结果
    all_area = []
    for i in range(len(area_list)):
        area = area_list[i]
        all_area.append(area.to_dict())
    return jsonify({'code': 200, 'msg': '请求成功！', 'data': all_area})


# 发布房源页面配套信息
@home_blue.route('/house_facility/', methods=['GET'])
@login_required
def house_facility():
    facility_list = Facility.query.all()
    # 组装
    all_facility = []
    for i in range(len(facility_list)):
        facility = facility_list[i]
        all_facility.append(facility.to_dict())
    return jsonify({'code': 200, 'msg': '请求成功！', 'data': all_facility})


# 发布新房源
@home_blue.route('/newhouse/', methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


# 发布新房源页面提交请求
@home_blue.route('/my_newhouse/', methods=['POST'])
@login_required
def my_newhouse():
    newhouse_info = request.form.to_dict()
    facilities = request.form.getlist('facility')
    user = User.query.filter_by(id=session['user_id']).first()
    house = House()
    # 向数据库存入数据
    house.user_id = user.id
    house.title = newhouse_info['title']
    house.area_id = newhouse_info['area_id']
    house.price = newhouse_info['price']
    house.address = newhouse_info['address']
    house.room_count = newhouse_info['room_count']
    house.acreage = newhouse_info['acreage']
    house.unit = newhouse_info['unit']
    house.capacity = newhouse_info['capacity']
    house.beds = newhouse_info['beds']
    house.deposit = newhouse_info['deposit']
    house.min_days = newhouse_info['min_days']
    house.max_days = newhouse_info['max_days']
    for i in range(len(facilities)):
        f = Facility.query.filter_by(id=facilities[i]).first()
        house.facilities.append(f)
    house.add_update()
    house_id = House.query.filter_by(user_id=session['user_id'], title=newhouse_info['title']).first().id
    return jsonify({'code': 200, 'msg': '请求成功！', 'data': {'house_id': house_id}})


# 新房源页面添加图片
@home_blue.route('/my_newhouse_img/', methods=['POST'])
@login_required
def my_newhouse_img():
    # 获取图片
    files = request.files.get('house_image')
    house_id = request.form.get('house_id')
    # 拼接图片完整地址
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    IMAGE_DIR = os.path.join(STATIC_DIR, 'images')
    filename = str(uuid.uuid4())
    a = files.mimetype.split('/')[-1:][0]
    imgname = filename + '.' + a
    path = os.path.join(IMAGE_DIR, imgname)

    # 向image里面保存图片
    files.save(path)

    # 向数据库保存图片
    house = House.query.filter_by(id=house_id).first()
    image = HouseImage()
    image.house_id = house_id
    image.url = '/static/' + 'images/' + imgname
    image.add_update()
    index_image = house.index_image_url
    if not index_image:
        house.index_image_url = '/static/' + 'images/' + imgname
        house.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})


@home_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@home_blue.route('/detail_info/', methods=['GET'])
def detail_info():
    house_id = request.args.get('house_id')
    house = House.query.filter_by(id=house_id).first()
    house_info = house.to_full_dict()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': house_info})


@home_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@home_blue.route('/index_info/', methods=['GET'])
def my_index():
    try:
        user_id = session['user_id']
        user_name = User.query.filter_by(id=user_id).first().name
    except Exception as e:
        user_name = ''
    image = House.query.all()
    all_image = [(i.id, i.title, i.index_image_url) for i in image]
    return jsonify({'code': 200, 'msg': '请求成功', 'data': {'user_name': user_name, 'all_image': all_image}})


@home_blue.route('/get_index_info/', methods=['POST'])
def get_index_info():
    return jsonify({'code': 200, 'msg': '请求成功'})


@home_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@home_blue.route('/search_info/', methods=['GET'])
def search_info():
    a_id = request.args.get('a_id')
    a_name = request.args.get('a_name')
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    all_order = Order.query.all()
    if not a_id:
        if not start_date:
            get_order_house_id = set(i.house_id for i in all_order)
            all_house = House.query.filter(House.id.in_(get_order_house_id)).all()
            all_houses = House.query.all()
            house_list = []
            for i in all_houses:
                if i not in all_house:
                    house_list.append(i.to_dict())
            return jsonify({'code': 200, 'msg': '没有id和开始时间', 'data': house_list})
        all_order = Order.query.all()
        return jsonify({'code': 200, 'msg': '没有id有时间'})
    if not start_date:
        return jsonify({'code': 200, 'msg': '有id没时间'})
    orders = []
    for order in all_order:
        if start_date <= order.begin_date and end_date >= order.end_date:
            orders.append(order)
        if start_date <= order.begin_date and end_date <= order.end_date:
            orders.append(order)
        if start_date >= order.begin_date and end_date >= order.end_date:
            orders.append(order)
        if start_date >= order.begin_date and end_date <= order.end_date:
            orders.append(order)
    orders = set(orders)

    return jsonify({'code': 200, 'msg': '请求成功'})
