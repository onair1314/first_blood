# -*- coding: utf-8 -*-
from dock_first_blood.server import db


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
