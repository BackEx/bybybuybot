import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField, PointField, FloatField, SequenceField, \
    BooleanField
from tornkts.base.mongodb.user import User as BaseUser
from tornkts.base.mongodb import BaseDocument
from tornkts.base.mongodb.user import BaseAdmin
from datetime import datetime
from pytz import timezone


class Admin(BaseAdmin):
    role = 'admin'
    meta = {
        'collection': role
    }


class Currency(BaseDocument):
    meta = {
        'indexes': [
            ('code', 'direct')
        ]
    }

    DIRECT_SALE = 'sale'
    DIRECT_BUY = 'buy'

    code = StringField()
    value = FloatField()
    direct = StringField(choices=[DIRECT_SALE, DIRECT_BUY])
    use_api = BooleanField(default=True)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'code': self.code,
            'value': self.value,
            'direct': self.direct,
            'use_api': self.use_api,
            'update_date': self.update_date
        }

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        self.value = float(self.value)
        return super(Currency, self).save(*args, **kwargs)


class Exchange(BaseDocument):
    out_id = IntField()
    title = StringField()
    phone = StringField()

    address = StringField()
    geo = PointField()

    active = BooleanField(default=False)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def get_rating(self):
        return Request.objects(exchange=self).average('rating_value')

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'out_id': self.out_id,
            'title': self.title,
            'phone': self.phone,
            'geo': self.geo,
            'address': self.address,
            'active': self.active,
            'creation_date': self.creation_date,
            'update_date': self.update_date,
            'rating': self.get_rating()
        }

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Exchange, self).save(*args, **kwargs)


class Request(BaseDocument):
    TYPE_BUY_USD = 'buy_usd'
    TYPE_SAIL_USD = 'sale_usd'
    TYPE_BUY_EUR = 'buy_eur'
    TYPE_SAIL_EUR = 'sale_eur'

    number = SequenceField(unique=True)

    user = ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY, required=False)
    exchange = ReferenceField('Exchange', reverse_delete_rule=mongoengine.NULLIFY, required=False)
    step = IntField(default=0)

    type = StringField(choices=[TYPE_SAIL_EUR, TYPE_SAIL_USD, TYPE_BUY_EUR, TYPE_BUY_USD])
    course = FloatField(default=0)
    amount = IntField(default=0)
    geo = PointField()

    external_id = IntField()

    rating_request_send = BooleanField(default=False)

    fail_sended = BooleanField(default=False)
    creation_date = DateTimeField()
    update_date = DateTimeField()

    rating_value = IntField(default=None)
    rating_comment = StringField(default='')
    distance = FloatField(default=None)

    date_commission_withdrawal = DateTimeField(default=None)
    exchange_confirm = BooleanField(default=False)

    def to_dict_impl(self, **kwargs):
        result = {
            'id': self.get_id(),
            'number': self.number,
            'external_id': self.external_id,
            'step': self.step,
            'type': self.type,
            'amount': self.amount,
            'geo': self.geo,
            'course': self.course,
            'creation_date': self.creation_date,
            'update_date': self.update_date,
            'rating_value': self.rating_value,
            'rating_comment': self.rating_comment,
            'distance': self.distance,
            'exchange': self.exchange.to_dict() if self.exchange is not None else False,
            'date_commission_withdrawal': self.date_commission_withdrawal if self.date_commission_withdrawal else None,
            'exchange_confirm': True if self.exchange_confirm else False
        }

        try:
            result['user'] = self.user.to_dict() if self.user else {}
        except:
            result['user'] = {}

        return result

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Request, self).save(*args, **kwargs)


class User(BaseUser):
    out_id = IntField(unique=True)

    name = StringField()
    surname = StringField()
    username = StringField()

    current_request = ReferenceField('Request', reverse_delete_rule=mongoengine.NULLIFY)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(User, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'out_id': self.out_id,
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'creation_date': self.creation_date
        }
