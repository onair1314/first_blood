# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
import json
from dock_first_blood.model.db import ProductCategory, Product

# 商品模块
blueprint = Blueprint('product', __name__, url_prefix='/first_blood/product')


@blueprint.route('/category',  methods=['GET', 'POST'])
def query_product_category():
    catagories = ProductCategory.query_product_category(0)
    print('catagories', catagories)
    catagories_dict = []
    # json.dumps方法不能对自定义对象直接序列化,首先把自定义对象转换成字典
    for category in catagories:
        catagory_dict = category.obj_2_dict()
        print('catagory_dict', catagory_dict)
        catagories_dict.append(catagory_dict)

    j_content = json.dumps(catagories_dict)
    return jsonify(meta={'code': 200}, data={'j_content': j_content})


# 根据类别id返回该类别下的所有商品
@blueprint.route('/products/<int:category_id>',  methods=['GET', 'POST'])
def query_products(category_id):
    content = request.values.get('content')

    products = Product.query_product_by_category_id(category_id)
    # json.dumps方法不能对自定义对象直接序列化,首先把自定义对象转换成字典
    return jsonify(meta={'code': 200}, products=[product.obj_2_dict() for product in products])


# 根据商品id返回该商品信息
@blueprint.route('/product/<int:product_id>',  methods=['GET', 'POST'])
def query_product(product_id):
    product = Product.query_product_by_product_id(product_id)
    product_dict = product.obj_2_dict()
    return jsonify(meta={'code': 200}, product=product_dict)
