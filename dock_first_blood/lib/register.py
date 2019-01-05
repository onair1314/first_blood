# -*- coding: utf-8 -*-
import hashlib
from Crypto.Cipher import AES
import base64
from dock_first_blood.model.config import blood_config


class AESCipher(object):
    # 加解密的密钥必须是16的倍数
    BS = 16

    def __init__(self, key):
        self.cipher = AES.new(key)

    def _pad(self, s):
        pad = AESCipher.BS - len(s) % AESCipher.BS
        return s + pad * chr(pad)

    def _unpad(self, s):
        pad = s[-1]
        return s[0:-ord(pad)]

    def encrypt(self, raw):
        raw = self._pad(raw)
        return self.cipher.encrypt(raw)

    def decrypt(self, enc):
        return self._unpad(self.cipher.decrypt(enc))


def decrypt_data(key, content):
    def b64_padding(raw_str):
        s_len = len(raw_str)
        if s_len % 4 == 0:
            return raw_str
        else:
            return '{raw_str}{padding}'.format(
                raw_str=raw_str,
                padding='=' * (4 - s_len % 4)
            )

    data = base64.decodestring(b64_padding(content.encode()))
    cipher = AESCipher(key.encode())
    return cipher.decrypt(data)


def encrypt_data(key, content):
    cipher = AESCipher(key.encode())
    return base64.b64encode(cipher.encrypt(content.encode()))


def verify_signature(sig, signature, content):
    # json content not python content
    sig_kvs = blood_config.sig_config
    key = sig_kvs.get(sig, {})
    if not key:
        return False
    hash_new = hashlib.sha256(key.encode())
    hash_new.update(content.encode())
    server_signature = hash_new.hexdigest()
    if signature == server_signature:
        return True
    return False
