"""
    flask_session.sessions
    ~~~~~~~~~~~~~~~~~~~~~~

    Server-side Sessions and SessionInterfaces.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""
from uuid import uuid4
try:
    import cPickle as pickle
except ImportError:
    import pickle

from flask.sessions import SessionInterface as FlaskSessionInterface
from flask.sessions import SessionMixin

from itsdangerous import Signer

from werkzeug.datastructures import CallbackDict


def default_parse_sid(app, request):
    return request.cookies.get(app.session_cookie_name)


def total_seconds(td):
    return td.days * 60 * 60 * 24 + td.seconds


class ServerSideSession(CallbackDict, SessionMixin):
    """Baseclass for server-side based sessions."""

    def __init__(self, initial=None, sid=None, new=False, refresh=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.refresh = refresh
        self.modified = False


class RedisSession(ServerSideSession):
    pass


class SessionInterface(FlaskSessionInterface):

    def _generate_sid(self, app):
        sid = str(uuid4())
        signer = self._get_signer(app)
        if signer is not None:
            sid = signer.sign(sid).decode('utf-8')
        return sid

    def _is_sid_legal(self, app, sid):
        signer = self._get_signer(app)
        if signer is not None:
            return signer.validate(sid)
        return True

    def _get_signer(self, app):
        if not app.secret_key:
            return None
        return Signer(app.secret_key, salt='flask-session',
                      key_derivation='hmac')


class NullSessionInterface(SessionInterface):
    """Used to open a :class:`flask.sessions.NullSession` instance.
    """

    def open_session(self, app, request):
        return None


class RedisSessionInterface(SessionInterface):
    """Uses the Redis key-value store as a session backend.

    .. versionadded:: 0.2
        The `use_signer` parameter was added.

    :param redis: A ``redis.Redis`` instance.
    :param key_prefix: A prefix that is added to all Redis store keys.
    """

    serializer = pickle
    session_class = RedisSession
    parse_sid = default_parse_sid

    def __init__(self, redis, key_prefix):
        self.redis = redis
        self.key_prefix = key_prefix

    def open_session(self, app, request):
        sid = self.parse_sid(app, request)
        if not sid or not self._is_sid_legal(app, sid):
            sid = self._generate_sid(app)
            return self.session_class(sid=sid, new=True)

        val = self.redis.get(self.key_prefix + sid)
        if val is not None:
            try:
                data = self.serializer.loads(val)
                return self.session_class(data, sid=sid)
            except:  # noqa E722
                return self.session_class(sid=sid, new=True)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                self.redis.delete(self.key_prefix + session.sid)
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
            return

        if (
            session.modified
            or (session.permanent and session.refresh)
        ):
            val = self.serializer.dumps(dict(session))
            self.redis.setex(
                name=self.key_prefix + session.sid,
                value=val,
                time=total_seconds(app.permanent_session_lifetime))

        if (
            session.new
            or (session.permanent and session.refresh)
        ):
            httponly = self.get_cookie_httponly(app)
            secure = self.get_cookie_secure(app)
            expires = self.get_expiration_time(app, session)
            response.set_cookie(app.session_cookie_name, session.sid,
                                expires=expires, httponly=httponly,
                                domain=domain, path=path, secure=secure)
