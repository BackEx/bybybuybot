# coding=utf-8
from models.awa import Request

CURRENCY_EXCHANGE = {
    Request.TYPE_BUY_USD: u'Купить $',
    Request.TYPE_SAIL_USD: u'Продать $',
    Request.TYPE_BUY_EUR: u'Купить €',
    Request.TYPE_SAIL_EUR: u'Продать €',
}

CURRENCY_EXCHANGE_QUESTION = {
    Request.TYPE_BUY_USD: u'Сколько $ вы хотите купить?',
    Request.TYPE_SAIL_USD: u'Сколько $ вы хотите продать?',
    Request.TYPE_BUY_EUR: u'Сколько € вы хотите купить?',
    Request.TYPE_SAIL_EUR: u'Сколько € вы хотите продать?',
}

STEP_ZERO = 0
STEP_INPUT_OPERATION = 1
STEP_INPUT_AMOUNT = 2
STEP_CONFIRM = 3
STEP_ENTER_GEO = 4
STEP_SEARCH_EXCHANGE = 5
STEP_SEARCH_SUCCESS = 6
STEP_SUCCESS_RESPONSE = 7
STEP_NO_RESPONSE = 100

