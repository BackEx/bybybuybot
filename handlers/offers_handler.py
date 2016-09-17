from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin

from base.base_handler import BankExObjectHandler
from base.base_server_error import BankExServerError
from models.awa import Salesman, Admin, Offer


class OffersHandler(AuthMixin, BankExObjectHandler):
    MODEL_CLS = Offer

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

    def publish(self):
        telegram_id = self.get_str_argument('telegram_id')
        try:
            salesman = Salesman.objects.get(telegram_id=telegram_id)
        except Salesman.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND,field='salesman')

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

        self.send_success_response(data={'id': offer.get_id()})
