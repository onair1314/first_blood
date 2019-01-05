# -*- coding: utf-8 -*-
# from flask import g
import yaml
import redis


class BloodConfig(object):

    def __init__(self):
        self._rds = None
        self._config = None

    @property
    def init_config(self):
        if self._config is None:
            with open('config.template.yaml', 'r') as f:
                config_yaml = yaml.load(f)
            self._config = config_yaml
        return self._config

    @property
    def main_config(self):
        return self.init_config.get('main', {})

    @property
    def sig_config(self):
        return self.main_config.get('request', {}).get('sig_keys', {})

    @property
    def rds(self):
        if self._rds is None:
            rds_config = self.main_config.get('redis', {})
            pool = redis.ConnectionPool(**rds_config)
            self._rds = redis.StrictRedis(connection_pool=pool)
        return self._rds


blood_config = BloodConfig()
