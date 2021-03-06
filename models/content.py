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
            'CL_MSG_WELCOME': u"""Привет! Теперь, если ты хочешь потратить свои деньги, тебе даже не нужно выпускать смартфон из рук! Просто напиши что ты хочешь. Твой город?""",
            'CL_MSG_ENTER_TAGS': u"""
Хештегами люди ищут информацию.
Смарттегами люди ищут сделки,
введи несколько смарттегов
которые наиболее соответствуют твоим желаниям:
образец - $smartteg1, $smartteg2, $smartteg3
""",
            'CL_MSG_ENTER_PRICE': u"""
Сколько примерно ты хотел бы заплатить за сделку?
Так как продавцом может быть иностранец, введи цифру в долларах
""",
            'CL_MSG_COMPLETE_FILL_INFO': u"""
Отлично!
Теперь бот будет тебе показывать офферы продавцов.
Для просмотра нажимай кнопки вперед-назад, а когда ты найдешь нужный тебе оффер жми - «Buy» и ты сможешь оформить сделку!
            """,
            'CL_MSG_ALL_UNDERSTAND': u"""Понял, начинаем поиск""",
            'CL_MSG_NEW_SEARCH': u"""Новый поиск""",
            'CL_MSG_PREVIOUS': u"""Назад""",
            'CL_MSG_NEXT': u"""Вперед""",
            'CL_MSG_IMAGE_NOT_FOUND': u"""Изображение лота не найдено""",
            'CL_MSG_NO_MORE': u"""Пока что нет больше предложений""",
            'CL_MSG_SEND_NUMBER': u"""Отправьте число""",
            'CL_MSG_NAV_HINT': u"""Подсказка: кнопками снизу ты можешь переходить между лотами или начать новый поиск""",
            'CL_MSG_CHOOSE_OFFER': u"""
Отлично! Ты выбрал оффер.
Исполнение твоей сделки гарантирует только история продавца, которая записана в распределенном реестре блокчейн.
В блокчейн пишется не только история продавца, но и твоя, как покупателя.
Регистрируем тебя в блокчейн?
""",
            'CL_YES_APPROVE': u"Да, подтверждаю",
            'CL_NO_FEAR': u"Нет, боюсь",
            'CL_WHAT_IS_BLOCKCHAIN': u"Что такое блокчейн?",
            'CL_FEAR_BLOCKCHAIN_WIKI': u"""
Ну что же, в первый раз всем страшно.
Почитай про блокчейн тут: https://ru.wikipedia.org/wiki/Цепочка_блоков_транзакций
            """,
            'CL_WHAT_IS_BLOCKCHAIN_WIKI': u""""
Ок, блокчейн - это цепочка блоков транзакций.
Все равно ничего не понял? Тогда читай тут: https://ru.wikipedia.org/wiki/Цепочка_блоков_транзакций
""",
            'CL_REG_QIWI': u"""
Окей!
Для того что бы легко потратить деньги онлайн, они тебе нужны в QIWI кошельке.
Давай его зарегистрируем, что бы пополнить баланс?
""",
            'CL_BEGIN_DEAL': u"""
"Отлично, теперь можно начинать сделку!
На смартфон продавца отправлено уведомление, подожди подтверждения."
""",
            'CL_WANT_SPENT_MONEY': u"Нет, не хочу тратить деньги легко",
            'CL_WHAT_IS_QIWI': u'Что такое QIWI-кошелек?',
            'CL_CANNOT_SPEND_MONEY': u"""
Без регистрации QIWI кошелька ты не сможешь легко потратить деньги на выбранный оффер.
Подумай об этом.
""",
            'CL_QIWI_DESCRIPTION': u"""
QIWI - это электронная платежная система, чтобы легче тратить деньги.
Почитай об этом здесь: https://ru.wikipedia.org/wiki/Qiwi и приходи к нам снова)
"""
        }
