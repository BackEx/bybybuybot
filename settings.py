# coding=utf-8
from tornado.options import define, options
import os

from roboman.bot import BaseBot

__author__ = 'grigory51'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_config(path):
    try:
        options.parse_config_file(path=path, final=False)
    except IOError:
        print '[WARNING] File no readable, run with default settings'


define('host', type=str, group='Server', default='127.0.0.1', help='Listen host')
define('port', type=int, group='Server', default=8080, help='Listen port')
define('server_name', type=str, group='Server', default='bankex.awa.finance')
define('server_schema', type=str, group='Server', default='http')

define('debug', type=bool, group='Server', default=False, help='Tornado debug mode')
define('config', type=str, group='Server', help='Path to config file', callback=parse_config)
define('runtime', type=str, group='Server', help='Data dir', default=CURRENT_DIR + '/runtime/')

define('static_root', type=str, group='Server', help='Data dir', default=CURRENT_DIR + '/admin/')
define('session_path', type=str, group='Server', default=CURRENT_DIR + '/runtime/sessions/')
define('upload_path', type=str, group='Server', default=CURRENT_DIR + '/uploads/')

define('mongo_uri', type=str, group='DB', default='mongodb://127.0.0.1:27017/bankex?connectTimeoutMS=1000&socketTimeoutMS=1000', help='Connection URI')

define('mode', type=str, group='Bots', default=BaseBot.MODE_GET_UPDATES)
define('update_interval', type=int, group='Bots', default=1000)
define('key_bank_ex_customer', type=str, group='Bots', default='207350618:AAFCsLMrEqEwcdHn4uqzSMfiTmtdLdTKs_M')

options.parse_command_line(final=True)
