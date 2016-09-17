import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField
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
