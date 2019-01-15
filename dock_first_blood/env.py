import os

import redis

import yaml

from .config import config
from .session import NullSessionInterface, RedisSessionInterface


class FlaskEnv(object):

    def __init__(self, app=None):
        self._config = None
        self._load_config()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app_config = {k.upper(): v for k, v in
                      self._config['flask']['app'].items()}
        app.config.update(app_config)
        for attr in dir(self):
            if attr.startswith('_init_'):
                getattr(self, attr)(app)

    def _load_config(self):
        config_path = os.path.join(os.path.abspath(os.getcwd()), 'config.yaml')
        with open(config_path, encoding='utf-8') as f:
            self._config = yaml.load(f)
            config.update(self._config)

    def _init_session(self, app):
        session_interface = NullSessionInterface()

        session_config = self._config['flask'].get('session')
        if session_config:
            if session_config['type'] == 'redis':
                redis_config = session_config['redis']
                redis_instance = redis.Redis(
                    host=redis_config['host'],
                    port=redis_config['port'],
                    db=redis_config['db']
                )
                RedisSessionInterface.parse_sid = parse_sid
                session_interface = RedisSessionInterface(
                    redis_instance, redis_config.get('key_prefix', ''))

        app.session_interface = session_interface


def parse_sid(app, request):
    sid = request.cookies.get(app.session_cookie_name)
    if not sid:
        authorization = request.headers.get('Authorization')
        if authorization:
            try:
                return authorization.split(' ', 1)[1]
            except:  # noqa
                pass
