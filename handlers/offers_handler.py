from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin

from base.base_handler import BankExObjectHandler, TemplateMixin
from base.base_server_error import BankExServerError
from models.awa import Salesman, Admin, Offer
from settings import options
from utils import gen_path, mkdir


class OffersHandler(AuthMixin, TemplateMixin, BankExObjectHandler):
    MODEL_CLS = Offer

    @property
    def get_methods(self):
        methods = {
            'html': self.html
        }
        methods.update(super(OffersHandler, self).get_methods)
        return methods

    @property
    def post_methods(self):
        methods = {
            'publish': self.publish
        }
        methods.update(super(OffersHandler, self).post_methods)
        return methods

    @property
    def put_fields(self):
        return {
            'title': {'field_type': 'str'},
            'description': {'field_type': 'str'},
            'location': {'field_type': 'str'},
            'price': {'field_type': 'str'}
        }

    @property
    def auth_classes(self):
        return [Admin]

    @need_role([Admin.role])
    def get_object(self):
        return super(OffersHandler, self).get_object()

    @need_role([Admin.role])
    def put_object(self, updated_object=None):
        super(OffersHandler, self).put_object(updated_object)

    @gen.coroutine
    def publish(self):
        telegram_id = self.get_str_argument('telegram_id')
        try:
            salesman = Salesman.objects.get(telegram_id=telegram_id)
        except Salesman.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND, field='salesman')

        photo_url = self.get_str_argument('photo_url')
        title = self.get_str_argument('title')
        description = self.get_str_argument('description')
        price = self.get_int_argument('price')
        tags = self.get_str_array_argument('tags')
        offer_type = self.get_str_argument('offer_type', allowed_values=Offer.OFFER_TYPES)
        location = self.get_str_argument('location')

        offer = Offer(
            salesman=salesman,
            title=title,
            price=price,
            description=description,
            photo_url=photo_url,
            location=location,
            offer_type=offer_type,
            tags=tags
        )
        offer.save()

        url = 'http://3007.vkontraste.ru/?url=http://{0}/api/offers.html?id={1}'.format(options.server_name, offer.get_id())
        client = AsyncHTTPClient()
        req = HTTPRequest(url)
        res = yield client.fetch(req)

        path = gen_path()
        mkdir(path.get('folder'))
        with open(path.get('fullname'), "w") as f:
            f.write(res.body)

        offer.rendered_img = path.get('relname')
        offer.save()

        self.send_success_response(data={'id': offer.get_id()})

    def html(self):
        try:
            offer = Offer.objects.get(id=self.get_mongo_id_argument('id'))
        except Offer.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND)

        self.render('offer.html', {'offer': offer})
