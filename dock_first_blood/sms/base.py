import random


class BaseSms(object):

    def send_verification_code(self, phone_number, length=6):
        start = 10 ** (length - 1)
        end = 10 ** length - 1
        code = random.randint(start, end)
        self.send(phone_number, code)
        return code

    def send(self, phone_number, msg):
        raise NotImplementedError
