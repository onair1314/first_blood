# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from datetime import datetime
import hashlib
import random
import base64
import requests
import json
import uuid
from dock_first_blood.lib.register import verify_signature, decrypt_data
from dock_first_blood.model.exceptions import return_function
from dock_first_blood.model.db import User
from dock_first_blood.model.config import blood_config
from dock_first_blood.server import db


blueprint = Blueprint('register', __name__, url_prefix='/first_blood/register')


@blueprint.route('/phone',  methods=['GET', 'POST'])
def phone():
    # redis & mysql query do not have 'try'
    json_content = request.values.get('content')
    signature = request.values.get('signature', '')
    sig_kv = request.values.get('sig_kv')
    if not verify_signature(sig_kv, signature, json_content):
        error_dict = return_function(400, 10000, 'signature error')
        return jsonify(meta=error_dict)
    content = json.loads(json_content)
    phone_num = content.get('phone_num')
    user = User.query.filter_by(phone_num=phone_num).first()
    if user:
        error_dict = return_function(400, 10001, '该手机号已注册')
        return jsonify(meta=error_dict)
    verify_code = random.randint(100000, 999999)
    vendor_content = {
        "mobile": phone_num,
        "code": verify_code
    }

    # TODO: this should config
    vendor_url = 'https://api.sms.jpush.cn/v1/codes'
    vendor_access_key = 'xxx'
    vendor_secret_access_key = 'xxx'
    base64_auth_string = vendor_access_key + vendor_secret_access_key
    headers = {
        'Authorization': base64.b64encode(base64_auth_string)
    }
    res = requests.post(vendor_url, data=vendor_content, headers=headers)
    if json.loads(res.text).get('msg_id') is None:
        error_dict = return_function(400, 10002, '验证码发送失败')
        return jsonify(meta=error_dict)
    # TODO: THE END

    redis_client = blood_config.rds
    redis_client.set(phone_num, verify_code)
    redis_client.expire(phone_num, 90)
    return jsonify(meta={'code': 200})


@blueprint.route('/validate/code',  methods=['GET', 'POST'])
def validate_code():
    # redis & mysql query do not have 'try'
    json_content = request.values.get('content')
    signature = request.values.get('signature', '')
    sig_kv = request.values.get('sig_kv')
    if not verify_signature(sig_kv, signature, json_content):
        error_dict = return_function(400, 10000, 'signature error')
        return jsonify(meta=error_dict)
    content = json.loads(json_content)
    phone_num = content.get('phone_num')
    verify_code = content.get('verify_code')
    device_id = content.get('device_id')
    redis_client = blood_config.rds
    redis_verify_code = redis_client.get(phone_num).decode()
    if redis_verify_code is None:
        error_dict = return_function(400, 10003, '验证码过期')
        return jsonify(meta=error_dict)
    if redis_verify_code != verify_code:
        error_dict = return_function(400, 10004, '验证码错误')
        return jsonify(meta=error_dict)
    user = User.query.filter_by(phone_num=phone_num).first()
    create_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 当前UTC时间
    temp = phone_num + verify_code + device_id + create_time
    hash_new = hashlib.sha256('first_blood'.encode())
    hash_new.update(temp.encode())
    user_token = hash_new.hexdigest()
    if user is None:
        try:
            new_user = User(phone_num=phone_num, device_id=device_id,
                            create_time=create_time, user_token=user_token)
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            error_dict = return_function(500, 10005, '数据库新增错误')
            return jsonify(meta=error_dict)
    elif user.user_id is None:
        try:
            old_user = User.query.filter_by(phone_num=phone_num).update(dict(
                device_id=device_id, create_time=create_time, user_token=user_token))
            db.session.commit()
        except:
            db.session.rollback()
            error_dict = return_function(500, 10006, '数据库更新错误')
            return jsonify(meta=error_dict)
    else:
        error_dict = return_function(400, 10007, '手机号已注册')
        return jsonify(meta=error_dict)
    return jsonify(meta={'code': 200}, data={'user_token': user_token})


@blueprint.route('/register/user',  methods=['GET', 'POST'])
def register_user():
    phone_num = request.values.get('phone_num')
    ciphertext = request.values.get('ciphertext')
    user = User.query.filter_by(phone_num=phone_num).first()
    if user is None:
        error_dict = return_function(400, 10008, '数据库中无该手机号')
        return jsonify(meta=error_dict)
    if user.user_token is None:
        error_dict = return_function(400, 10009, '数据库中无该手机号的token')
        return jsonify(meta=error_dict)
    secret_key = user.user_token
    decrypt_dict = decrypt_data(secret_key, ciphertext)
    user_password = decrypt_dict.get('password')
    if user_password is None:
        error_dict = return_function(400, 10010, '解密失败')
        return jsonify(meta=error_dict)
    user_id = str(uuid.uuid1()).replace('-', '')
    last_login_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    try:
        old_user = User.query.filter_by(phone_num=phone_num).update(dict(
            user_password=user_password, user_id=user_id, last_login_time=last_login_time))
        db.session.commit()
    except:
        db.session.rollback()
        error_dict = return_function(500, 10011, '数据库更新uuid错误')
        return jsonify(meta=error_dict)
    return jsonify(meta={'code': 200}, data={'user_id': user_id})
