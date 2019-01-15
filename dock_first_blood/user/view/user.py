import datetime

from flask import Blueprint, g, request, session

from ..exceptions import return_error, return_json
from ..lib import User, is_phone_number_registered, is_phone_number_valid, sms


bp = Blueprint('user', __name__)


@bp.before_request
def before_request():
    session.permanent = True
    session.refresh = True
    g.jsondata = request.values or request.get_json()


@bp.route('/send_code', methods=['POST'])
def send_code():
    """发送验证码。

    Parameters
    ----------
    phone_number: str

    """
    code_expired_at = session.get('code_expired_at')
    if code_expired_at and datetime.datetime.utcnow() < code_expired_at:
        return_error('VerificationCodeHasSent')

    phone_number = g.jsondata.get('phone_number')
    if not is_phone_number_valid(phone_number):
        return_error('PhoneNumberInvalid')

    if is_phone_number_registered(phone_number):
        return_error('PhoneNumberRegistered')

    code = sms.send_verification_code(phone_number)
    session['phone_number'] = phone_number
    session['code'] = int(code)
    session['code_expired_at'] = (datetime.datetime.utcnow() +
                                  datetime.timedelta(seconds=70))
    return_json()


@bp.route('/validate_code', methods=['POST'])
def validate_code():
    """检验验证码。

    Parameters
    ----------
    code: int

    """
    code_expired_at = session.get('code_expired_at')
    if not code_expired_at:
        return_error('VerificationCodeNotSend')

    now = datetime.datetime.utcnow()
    if now > code_expired_at:
        return_error('VerificationCodeExpired')

    code = int(g.jsondata.get('code'))
    if code == session.get('code'):
        session['code_checked'] = True
        return_json()
    return_error('VerificationCodeInvalid')


@bp.route('/signup', methods=['POST'])
def signup():
    """注册

    Parameters
    ----------
    password: str

    """
    if not session.get('code_checked'):
        return_error('VerificationCodeNotCheck')

    password = g.jsondata.get('password')
    if not password:
        return_error('PasswordEmpty')

    phone_number = session['phone_number']
    user = User.create(phone_number, password)
    session.clear()
    session['user_id'] = user.user_id
    return_json(token=session.sid)


@bp.route('/login_by_password', methods=['POST'])
def login_by_password():
    data = g.jsondata()
    phone_number = data.get('phone_number')
    if not phone_number:
        return_error('PhoneNumberEmpty')
    if not is_phone_number_valid(phone_number):
        return_error('PhoneNumberInvalid')

    password = data.get('password')
    if not password:
        return_error('PasswordEmpty')

    user = User.get_by_phone_number(phone_number)
    if not user:
        return_error('UserNotExisted')

    session.clear()
    session['user_id'] = user.user_id
    return_json(token=session.sid)


@bp.route('/login_by_code', methods=['POST'])
def login_by_code():
    if not session.get('code_checked'):
        return_error('VerificationCodeNotCheck')

    phone_number = session['phone_number']
    user = User.get_by_phone_number(phone_number)
    if not user:  # shouldn't happen
        return_error('UserNotExisted')

    session.clear()
    session['user_id'] = user.user_id
    return_json(token=session.sid)
