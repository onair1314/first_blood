# -*- coding: utf-8 -*-
import datetime
import random

import bcrypt

from flask_mongoengine import MongoEngine


db = MongoEngine()


class UserError(Exception):
    pass


class UserPhoneNumberExistedError(UserError):
    pass


def to_bytes(s, encoding='utf-8'):
    pass


class User(db.Document):
    meta = {
        'indexes': [
            {
                'fields': ['user_id'],
                'unique': True,
            },
            {
                'fields': ['user_name'],
                'unique': True,
                'sparse': True,
            },
            {
                'fields': ['phone_number'],
                'unique': True,
            },
        ]
    }

    phone_number = db.StringField()
    user_password = db.StringField()
    user_id = db.StringField()
    user_name = db.StringField()
    device_ids = db.ListField(db.StringField())
    last_login_time = db.DateTimeField()
    crete_time = db.DateTimeField()
    update_time = db.DateTimeField()

    @classmethod
    def create(
        cls,
        phone_number,
        user_password,
        user_name=None,
        device_id=None
    ):
        if cls.is_phone_number_existed(phone_number):
            raise UserPhoneNumberExistedError(
                'The phone number: %s has existed' % phone_number)

        user = cls(phone_number=phone_number)
        user.user_password = bcrypt.hashpw(
            to_bytes(user_password), bcrypt.gensalt(12))
        user.user_id = cls.generate_user_id()
        user.user_name = user_name

        now = datetime.datetime.utcnow()
        user.create_time = now
        user.update_time = now
        user.last_login_time = now

        user.save()

    def check_password(self, password):
        return bcrypt.checkpw(to_bytes(password), self.user_password)

    @classmethod
    def is_phone_number_existed(cls, phone_number):
        obj = cls.objects(
            phone_number=phone_number
        ).only(
            'phone_number'
        ).first()
        if obj:
            return True
        return False

    @classmethod
    def generate_user_id(cls):
        user_id = int(random.random() * 100000000)
        while True:
            obj = cls.objects(
                user_id=user_id
            ).only(
                'user_id'
            ).first()
            if obj:
                user_id = int(random.random() * 100000000)
            else:
                break
        return user_id
