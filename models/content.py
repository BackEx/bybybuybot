# coding=utf-8
from datetime import datetime

from pytz import timezone
from tornkts.base.mongodb import BaseDocument
from mongoengine import StringField, DateTimeField, IntField


class Text(BaseDocument):
    key = StringField(required=True, unique=True)
    value = StringField(required=True)
    comment = StringField()

    update_date = DateTimeField()

    def save(self, *args, **kwargs):
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Text, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'key': self.key,
            'value': self.value,
            'comment': self.comment,
            'update_date': self.update_date
        }

    @staticmethod
    def get(key):
        try:
            return Text.objects.get(key=key)
        except:
            return False

    @classmethod
    def format(cls, key, *args):
        try:
            text = Text.get(key)
            if text == False:
                text = cls.defaults().get(key, '')
            else:
                text = text.value
            return text.format(*args)
        except:
            return ''

    @staticmethod
    def defaults():
        return {
            'CL_MSG_WELCOME': u'Привет, теперь если ты хочешь потратить деньги прямо здесь и сейчас - тебе даже не нужно доставать свою кредитку. просто напиши в боте что ты хочешь',
            'CL_SEND_GEO': u'Отправьте свою гео-позицию, чтобы мы могли подобрать для вас ближайший обменник',
            'CL_RESERV': u'Спасибо. Мы резервируем для вас курс и сумму в ближайшем обменнике. Это может занять до 15 минут',
            'CL_SUCCESS_RESERV': u"""
Спасибо. Ваш заказ подтвержден пунктом обмена валюты.
Адрес пункта обмена валюты: {0}
Телефон: {1}
Номер вашего заказа: {2}
Сообщите номер заказа в обменнике""",
            'CL_SUCCESS_WARNING': u"Внимание! Чтобы воспользоваться зафиксированным курсом, нужно совершить операцию не позже {0}",
            'CL_FAIL_RESERV': u'К сожалению мы не смогли найти обменник в радиусе 20 км.',
            'CL_FAIL_RESERV_TIMEOUT': u'Извините. Мы не смогли подтвердить ваш курс. Попробуйте, пожалуйста, еще раз ',
            'CL_REQUEST_RATING': u'Оцените, пожалуйста, как вас обслужили',
            'CL_RATING_COMMENT_REQUEST': u'Мы сожалеем и обещаем исправиться. Сообщите, что пошло не так.',
            'CL_RATING_COMMENT_GOOD': u'Спасибо! Хорошего дня!',
            'CL_RATING_COMMENT_GOOD_DAY': u'Хорошего дня!',
            'CL_CONFIRM_YES': u'Да, подтверждаю',
            'CL_CONFIRM_NO': u'Нет, отменить операцию',
            'CL_OPERATION_CANCEL': u'Операция отменена. Введите /start, чтобы начать заново',
            'CL_CONFIRM': u'Хорошо! Вы {0} {1}{2} по курсу {3} за {4} руб. Подвердите.',
            'CL_CONFIRM_REPEAT': u'Подтвердите или отмените операцию',
            'CL_ORDER_FORMED': u'Вы сформировали заказ на обмен валюты в пункте обмена по указанным выше контактным данным',
            'CL_NEW_EXCHANGE': u'Новый обмен',
        }
