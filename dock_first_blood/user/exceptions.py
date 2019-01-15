from flask import jsonify


def return_json(**kwargs):
    if 'code' not in kwargs:
        kwargs['code'] = 200
    return jsonify({'meta': kwargs})


def return_error(error_type):
    code, error_message = user_exceptions.get(error_type, (0, 'Unknown.'))
    return_json(code=code, error_type=error_type, error_message=error_message)


user_exceptions = {
    'VerificationCodeHasSent': (
        1000,
        'The verification code has been sent, please try again later.'
    ),
    'VerificationCodeExpired': (
        1001,
        'The verification code has been expired.'
    ),
    'VerificationCodeNotSend': (
        1002,
        'Please send code first.'
    ),
    'VerificationCodeInvalid': (
        1003,
        'The verification code you send is invalid.'
    ),
    'VerificationCodeNotCheck': (
        1004,
        'Please validate verification code first.'
    ),
    'PhoneNumberInvalid': (
        2000,
        'The phone number is invalid.'
    ),
    'PhoneNumberRegistered': (
        2001,
        'The phone number has been registered.'
    ),
    'PhoneNumberEmpty': (
        2002,
        "The phone number can't be empty."
    ),
    'PasswordEmpty': (
        3000,
        "The password can't be empty."
    ),
    'UserNotExisted': (
        4000,
        "The user doesn't exist."
    ),
}
