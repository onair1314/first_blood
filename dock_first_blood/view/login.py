# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from dock_first_blood.lib.register import verify_signature
from dock_first_blood.model.exceptions import return_function
from dock_first_blood.model.db import User
from dock_first_blood.server import db


blueprint = Blueprint('login', __name__, url_prefix='/first_blood/login')


@blueprint.route('/phone_num',  methods=['GET', 'POST'])
def login_phone_num():
    json_content = request.values.get('content')
    signature = request.values.get('signature', '')
    sig_kv = request.values.get('sig_kv')
    if not verify_signature(sig_kv, signature, json_content):
        error_dict = return_function(400, 10012, 'signature error')
        return jsonify(meta=error_dict)
    content = json.loads(json_content)
    phone_num = content.get('phone_num')
    user_password = content.get('password')
    device_id = content.get('device_id')
    user = User.get_user(phone_num)
    if user is None or user.user_token is None or user.user_id is None:
        error_dict = return_function(400, 10013, '数据库中无该手机号')
        return jsonify(meta=error_dict)
    if user_password != user.user_password:
        error_dict = return_function(400, 10014, '密码错误')
        return jsonify(meta=error_dict)
    last_login_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    user.last_login_time = last_login_time
    try:
        User.get_user(phone_num).update_user(dict(
            user_password=user_password, device_id=device_id, last_login_time=last_login_time))
    except:
        error_dict = return_function(500, 10015, '数据库更新device_id错误')
        return jsonify(meta=error_dict)
    return jsonify(meta={'code': 200}, data={'user_token': user.user_token,
                                             'user_id': user.user_id})
