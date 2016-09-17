# coding=utf-8
from content import awa_client
from models.awa import User, Request, Currency
from models.content import Text
from roboman.bot import BaseBot
from roboman.keyboard import ReplyKeyboard
import logging
from settings import options

logger = logging.getLogger('bank_ex_customer')


class BankExCustomer(BaseBot):
    name = 'TestBankExCustomer'
    key = options.key_bank_ex_customer

    @classmethod
    def num_split(cls, num):
        s = '%d' % num
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ' '.join(reversed(groups))

    @classmethod
    def before_hook(cls, data):
        try:
            user = User.objects.get(out_id=data.get('from_id'))
            user.username = data.get('from_username')
            user.save()
        except User.DoesNotExist:
            user = User(
                out_id=data.get('from_id'),
                name=data.get('from_first_name'),
                surname=data.get('from_last_name'),
                username=data.get('from_username')
            )
            user.save()

        data['user'] = user
        return data

    @classmethod
    def on_hook(cls, data):
        user = data['user']

        if user.current_request is None or Request.objects(pk=user.current_request.id).count() == 0:
            request = Request(user=user)
            request.save()
            user.current_request = request
            user.save()
        else:
            request = Request.objects.get(pk=user.current_request.id)

        request.user = user
        data['request'] = request
        text = data.get('text')

        if cls.match_command('/start', text):
            cls._on_start(**data)

    @classmethod
    def _on_start(cls, **kwargs):
        cls.send(
            chat_id=kwargs.get('chat_id'),
            text=Text.format('CL_MSG_WELCOME'),
        )