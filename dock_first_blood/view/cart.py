from flask import Blueprint, request, jsonify
import json
from dock_first_blood.model.db import CartInfo, Product
from dock_first_blood.model.exceptions import return_function

# 购物车模块
blueprint = Blueprint('cart', __name__, url_prefix='/first_blood/cart')


# 查看购物车
@blueprint.route('/cart',  methods=['GET', 'POST'])
def cart():
    content = request.values.get('content')
    j_content = json.loads(content)
    phone_num = j_content.get('phone_num')

    product_list = CartInfo.get_product_list(phone_num)
    products_dict = []
    if product_list is not None:
        # json.dumps方法不能对自定义对象直接序列化,首先把自定义对象转换成字典
        for product in product_list:
            product_dict = product.obj_2_dict()
            products_dict.append(product_dict)

    j_content = json.dumps(products_dict)
    return jsonify(meta={'code': 200}, data={'j_content': j_content})


# 加入购物车，不对金额进行任何的运算。
@blueprint.route('/add_to_cart',  methods=['GET', 'POST'])
def add_to_cart():
    content = request.values.get('content')
    j_content = json.loads(content)
    phone_num = j_content.get('phone_num')
    product_id = j_content.get('product_id')
    product = Product.query_product_by_product_id(product_id)

    try:
        CartInfo.add_product(phone_num, product)
    except:
        error_dict = return_function(600, 10001, '添加购物车错误')
        return jsonify(meta=error_dict)
    return jsonify(meta={'code': 200})
