from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required

from app.models import Order, User, House

order_blue = Blueprint('order', __name__)


@order_blue.route('/booking/', methods=['GET'])
@login_required
def booking():
    return render_template('booking.html')


@order_blue.route('/booking/', methods=['POST'])
@login_required
def my_booking():
    # 获取数据
    house_id = request.form.get('house_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    order_price = request.form.get('order_price')
    one_price = request.form.get('one_price')
    all_price = order_price.split('(')[0]
    day = order_price.split('共')[1].split('晚')[0]

    # 存入数据库
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = day
    order.house_price = one_price
    order.amount = all_price
    order.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})


@order_blue.route('/my_order/', methods=['GET'])
@login_required
def order():
    return render_template('orders.html')


@order_blue.route('/my_order_info/', methods=['GET'])
@login_required
def my_order():
    order_list = Order.query.filter_by(user_id=session['user_id']).all()
    all_order = []
    for i in range(len(order_list)):
        for status in [("WAIT_ACCEPT", '待接单'), ("WAIT_PAYMENT", '待支付'), ("PAID", '已支付'),
                       ("WAIT_COMMENT", '待评价'), ("COMPLETE", '已完成'), ("CANCELED", '已取消'),
                       ("REJECTED", '已拒单')]:
            if order_list[i].to_dict()['status'] == status[0]:
                dict = order_list[i].to_dict()
                dict['status'] = status[1]
                break
        all_order.append(dict)

    return jsonify({'code': 200, 'msg': '请求成功！', 'data': all_order})


@order_blue.route('/other_order/', methods=['GET'])
@login_required
def other_order():
    return render_template('lorders.html')


@order_blue.route('/other_order_info/', methods=['GET'])
@login_required
def other_order_info():
    houses = House.query.filter_by(user_id=session['user_id']).all()
    all_house_id = [house.id for house in houses]
    order_list = Order.query.filter(Order.house_id.in_(all_house_id)).all()
    all_order = []
    for i in range(len(order_list)):
        for status in [("WAIT_ACCEPT", '待接单'), ("WAIT_PAYMENT", '待支付'), ("PAID", '已支付'),
                       ("WAIT_COMMENT", '待评价'), ("COMPLETE", '已完成'), ("CANCELED", '已取消'),
                       ("REJECTED", '已拒单')]:
            if order_list[i].to_dict()['status'] == status[0]:
                dict = order_list[i].to_dict()
                dict['status'] = status[1]
                break
        all_order.append(dict)
    return jsonify({'code': 200, 'msg': '请求成功', 'data': all_order})


@order_blue.route('/order_status/', methods=['POST'])
@login_required
def order_status():
    status = request.form.get('my_status')
    order_id = request.form.get('my_id')
    order_comment=request.form.get('order_comment')
    order = Order.query.filter_by(id=order_id).first()
    order.status = status
    if order_comment:
        order.comment=order_comment
    order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})
