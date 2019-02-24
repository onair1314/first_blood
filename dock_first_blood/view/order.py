# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
import json
from dock_first_blood.model.db import Product, Order, OrderDetail, CartInfo
from dock_first_blood.model.exceptions import return_function

# 订单模块
blueprint = Blueprint('order', __name__, url_prefix='/first_blood/order')


@blueprint.route('/pay',  methods=['GET', 'POST'])
def pay():
    content = request.values.get('content')
    j_content = json.loads(content)
    user_id = j_content.get('user_id')

    cart_info = CartInfo.get_cart_info(user_id)
    if cart_info is None or cart_info.product_list is None:
        error_dict = return_function(600, 10001, '购物车中没有可支付的商品')
        return jsonify(meta=error_dict)

    # 创建订单
    order = Order()
    order.user_id = user_id
    order.status = 0
    order.quantity = len(cart_info.product_list)
    amount = 0
    ptotal = 0
    order_detail_list = []
    # 创建订单明细记录
    for product in cart_info.product_list:
        # 检查商品库存
        now_product = Product.query_product_by_product_id(product.id)
        if now_product is None or now_product.stock < product.buyCount:
            error_dict = return_function(600, 10002, '商品库存不足')
            return jsonify(meta=error_dict)
        order_detail = OrderDetail()
        order_detail.product_id = product.id
        order_detail.order_id = order.id
        order_detail.quantity = product.buyCount
        order_detail.price = product.now_price
        order_detail.total = order_detail.quantity * order_detail.price
        order_detail.fee = 0
        order_detail_list.append(order_detail)
        ptotal = ptotal + order_detail.total
        fee = fee + order_detail.fee

    order.amount = ptotal + fee
    order.ptotal = ptotal
    order.fee = fee
    # 插入订单表
    try:
        order_id = Order.create_order(order)
        for order_detail in order_detail_list:
            # 插入订单详情表
            OrderDetail.order_id = order_id
            OrderDetail.create_order_detail(order_detail)
    except:
        error_dict = return_function(600, 10003, '新增订单错误')
        return jsonify(meta=error_dict)

    return jsonify(meta={'code': 200}, data={'order_id': order_id})
