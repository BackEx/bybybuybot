import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField, ListField
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


class Salesman(BaseDocument):
    meta = {
        'indexes': [
            {
                'fields': ['telegram_id'],
                'unique': True
            }
        ]
    }

    telegram_id = StringField(required=True)
    telegram_nick = StringField()
    about = StringField()

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'telegram_id': self.telegram_id,
            'telegram_nick': self.telegram_nick,
            'about': self.about,
            'creation_date': self.creation_date,
            'update_date': self.update_date
        }

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Salesman, self).save(*args, **kwargs)


class Offer(BaseDocument):
    TYPE_ONLINE_VIDEO = 'online_video'
    TYPE_ONLINE_AUDIO = 'online_audio'
    TYPE_ONLINE_CHAT = 'online_chat'
    TYPE_OFFLINE = 'offline'

    OFFER_TYPES = [TYPE_ONLINE_VIDEO, TYPE_ONLINE_AUDIO, TYPE_ONLINE_CHAT, TYPE_OFFLINE]

    salesman = ReferenceField(Salesman, reverse_delete_rule=mongoengine.NULLIFY, required=False)

    title = StringField(required=True)
    price = IntField(required=True)
    description = StringField()
    photo_url = StringField()
    location = StringField()
    offer_type = StringField(choices=OFFER_TYPES)
    tags = ListField(StringField())

    creation_date = DateTimeField()
    update_date = DateTimeField()

    @property
    def type_title(self):
        if self.offer_type == self.TYPE_ONLINE_VIDEO:
            return 'Online video'
        elif self.offer_type == self.TYPE_ONLINE_AUDIO:
            return 'Online audio'
        elif self.offer_type == self.TYPE_ONLINE_CHAT:
            return 'Online chat'
        else:
            return 'Offline'

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Offer, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'photo_url': self.photo_url,
            'location': self.location,
            'offer_type': self.offer_type,
            'tags': ", ".join(self.tags),
            'creation_date': self.creation_date,
            'salesman_telegram_id': self.salesman.telegram_id if self.salesman else None,
            'salesman_id': self.salesman.get_id() if self.salesman else None,
        }


class User(BaseUser):
    out_id = IntField(unique=True)

    name = StringField()
    surname = StringField()
    username = StringField()

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
