from handlers.admin_handler import AdminHandler
from handlers.currency_handler import CurrencyHandler
from handlers.exchanges_handler import ExchangesHandler
from handlers.requests_handler import RequestsHandler
from handlers.texts_handler import TextsHandler
from os import path
from handlers.index_handler import IndexHandler
from mongoengine import connection as mongo_connection

from handlers.users_handler import UsersHandler
from roboman.server import RobomanServer
from settings import options
from bots.bankexcustomer import BankExCustomer
from tornado.web import StaticFileHandler

if __name__ == "__main__":
    bots = [
        BankExCustomer,
    ]

    handlers = [
        (r'/api/(logout)', AdminHandler),
        (r'/api/admin.(.*)', AdminHandler),
        (r'/api/currency.(.*)', CurrencyHandler),
        (r'/api/requests.(.*)', RequestsHandler),
        (r'/api/exchanges.(.*)', ExchangesHandler),
        (r'/api/texts.(.*)', TextsHandler),
        (r'/api/users.(.*)', UsersHandler),

        (r'/static/(.*)', StaticFileHandler, dict(path=path.join(options.static_root, 'static'))),
        (r'/(.*)', IndexHandler),
    ]

    settings = {
        'session': {
            'driver': 'file',
            'driver_settings': {
                'host': options.session_path
            },
            'cookie_config': {
                'expires_days': 365
            },
            'force_persistence': True,
            'cache_driver': True
        }
    }

    mongo_connection.connect(host=options.mongo_uri)
    server = RobomanServer(bots=bots, mode=options.mode, handlers=handlers, settings=settings)
    server.start()
