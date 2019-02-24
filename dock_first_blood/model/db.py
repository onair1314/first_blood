# -*- coding: utf-8 -*-
from dock_first_blood.server import db
from dock_first_blood.model.config import blood_config
import pickle


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_num = db.Column(db.String(11), index=True, unique=True)
    device_id = db.Column(db.String(100))
    create_time = db.Column(db.String(30))
    user_token = db.Column(db.String(32))
    user_id = db.Column(db.String(32), index=True, unique=True)
    user_password = db.Column(db.String(20))
    last_login_time = db.Column(db.String(30))
    user_name = db.Column(db.String(20))

    @property
    def device_list(self):
        return [x for x in self.device_id.split(';')]

    @device_list.setter
    def device_list(self, value):
        if self.device_id is None:
            self.device_id = value
        else:
            self.device_id += ';%s' % value

    def get_user(self, phone_num):
        return User.query.filter_by(phone_num=phone_num).first()

    def add_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception

    def update_user(self, update_args):
        try:
            self.update(update_args)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception


# 定义ProductCategory对象，商品类别类:
class ProductCategory(db.Model):
    # 表的名字:
    __tablename__ = 'product_category'

    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    code = db.Column(db.String(20))
    category_order = db.Column(db.String(50))
    parent_id = db.Column(db.Integer)
    show_in_nav = db.Column(db.String(1))

    def obj_2_dict(self):
        catagory_dict = {}
        catagory_dict['id'] = self.id
        catagory_dict['name'] = self.name
        catagory_dict['code'] = self.code
        catagory_dict['category_order'] = self.category_order
        catagory_dict['parent_id'] = self.parent_id
        catagory_dict['show_in_nav'] = self.show_in_nav
        if self.children is not None:
            catagory_dict['children'] = [child.obj_2_dict() for child in self.children]
        else:
            catagory_dict['children'] = ''
        return catagory_dict

    @classmethod
    def query_product_category(cls, parent_id):
        categories = ProductCategory.query.filter_by(ProductCategory.parent_id == parent_id).all()
        if len(categories) == 0:
            return None
        for category in categories:
            category.children = ProductCategory.query_product_category(category.id)
        return categories


# 定义Product对象，商品类:
class Product(db.Model):
    # 表的名字:
    __tablename__ = 'product'

    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    introduction = db.Column(db.String(20))
    price = db.Column(db.Numeric)
    now_price = db.Column(db.Numeric)
    picture = db.Column(db.String(50))
    create_time = db.Column(db.TIMESTAMP)
    sale = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    buyCount = 0           # 购买该类产品的总数

    @classmethod
    def query_product_by_category_id(cls, category_id):
        products = Product.query.filter_by(Product.category_id == category_id).all()
        print('len(products)', len(products))
        if len(products) == 0:
            return None
        return products

    @classmethod
    def query_product_by_product_id(cls, product_id):
        product = Product.query.filter_by(Product.id == product_id).one()
        return product

    def obj_2_dict(self):
        product_dict = {}
        product_dict['id'] = self.id
        product_dict['status'] = self.status
        product_dict['category_id'] = self.category_id
        product_dict['name'] = self.name
        product_dict['introduction'] = self.introduction
        product_dict['price'] = str(self.price)
        product_dict['now_price'] = str(self.now_price)
        product_dict['picture'] = self.picture
        product_dict['create_time'] = str(self.create_time)
        product_dict['sale'] = self.sale
        product_dict['stock'] = self.stock
        product_dict['buyCount'] = self.buyCount
        return product_dict


# 定义Order 对象，订单类:
class Order(db.Model):
    # 表的名字:
    __tablename__ = 'order'

    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    # order_id = db.Column(db.String(20))
    amount = db.Column(db.Numeric)
    ptotal = db.Column(db.Numeric)
    fee = db.Column(db.Numeric)

    def create_order(self, order):
        try:
            db.session.add(order)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception


#  定义OrderDetail对象，订单详情类:
class OrderDetail(db.Model):
    # 表的名字:
    __tablename__ = 'order_detail'

    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20))
    product_id = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    total = db.Column(db.Numeric)
    fee = db.Column(db.Numeric)

    def create_order_detail(self, order_detail):
        try:
            db.session.add(order_detail)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception


# 定义CartInfo对象，Redis里的购物车类:
class CartInfo:
    def __init__(self, product_list, amount):
        self.product_list = product_list     # 购物车中商品列表
        self.amount = amount            # 合计总金额

    @classmethod
    def get_cart_info(cls, user_id):
        redis_client = blood_config.rds
        result = redis_client.get(str(user_id) + '_' + 'cart_info')
        if result is None:
            return None
        else:
            cart_info = pickle.loads(result)
            return cart_info

    @classmethod
    def get_product_list(cls, user_id):
        redis_client = blood_config.rds
        result = redis_client.get(str(user_id) + '_' + 'cart_info')
        if result is None:
            return None
        else:
            cart_info = pickle.loads(result)
            return cart_info.product_list

    @classmethod
    def add_product(cls, user_id, product):
        try:
            redis_client = blood_config.rds
            redis_key = str(user_id) + '_' + 'cart_info'
            result = redis_client.get(redis_key)
            if result is None:
                cart_info = CartInfo([], 0)
            else:
                cart_info = pickle.loads(result)
            has_product = False
            for old_product in cart_info.product_list:
                if old_product.id == product.id:
                    old_product.buyCount = old_product.buyCount + 1
                    has_product = True
                    break
            if has_product is False:
                product.buyCount = 1
                cart_info.product_list.append(product)
            p_str = pickle.dumps(cart_info)
            redis_client.set(redis_key, p_str)  # 添加到redis
        except:
            raise Exception
