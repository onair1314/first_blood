import base64

from itsdangerous import want_bytes

import requests

from .base import BaseSms
from .exceptions import SmsSendError


class JpushSms(BaseSms):
    url = 'https://api.sms.jpush.cn/v1/codes'

    def __init__(self, access_key, secret_access_key):
        base64_auth_string = access_key + secret_access_key
        self.headers = {
            'Authorization': base64.b64encode(want_bytes(base64_auth_string))
        }

    def send(self, phone_number, msg):
        data = {
            'mobile': phone_number,
            'code': msg
        }
        res = requests.post(self.url, data=data, headers=self.headers)
        try:
            res.raise_for_status()
        except Exception as e:
            raise SmsSendError(str(e))

        res_data = res.json()
        if 'msg_id' not in res_data:
            raise SmsSendError('Sending message failed.')
