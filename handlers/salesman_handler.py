from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin

from base.base_handler import BankExObjectHandler
from base.base_server_error import BankExServerError
from models.bankex import Salesman, Admin


class SalesmanHandler(AuthMixin, BankExObjectHandler):
    MODEL_CLS = Salesman

    @property
    def post_methods(self):
        methods = {
            'register': self.register,
            'update': self.update_salesman
        }
        methods.update(super(SalesmanHandler, self).post_methods)
        return methods

    @property
    def put_fields(self):
        return {
            'telegram_nick': {'field_type': 'str'},
            'about': {'field_type': 'str'},
        }

    @property
    def auth_classes(self):
        return [Admin]

    @need_role([Admin.role])
    def get_object(self):
        return super(SalesmanHandler, self).get_object()

    @need_role([Admin.role])
    def put_object(self, updated_object=None):
        super(SalesmanHandler, self).put_object(updated_object)

    def register(self):
        telegram_id = self.get_str_argument('telegram_id')
        telegram_nick = self.get_str_argument('telegram_nick')
        about = self.get_str_argument('about', default=None)

        try:
            Salesman.objects.get(telegram_id=telegram_id)
            raise BankExServerError(BankExServerError.ALREADY_EXIST)
        except Salesman.DoesNotExist:
            pass

        salesman = Salesman(telegram_id=telegram_id, telegram_nick=telegram_nick, about=about)
        salesman.save()
        self.send_success_response(data={'id': salesman.get_id()})

    def update_salesman(self):
        telegram_id = self.get_str_argument('telegram_id')

        try:
            salesman = Salesman.objects.get(telegram_id=telegram_id)
        except Salesman.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND)

        telegram_nick = self.get_str_argument('telegram_nick', default=None)
        about = self.get_str_argument('about', default=None)

        if telegram_nick:
            salesman.telegram_nick = telegram_nick
        if about:
            salesman.about = about

        salesman.save()