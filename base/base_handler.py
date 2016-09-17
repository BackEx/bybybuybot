from tornkts import utils
from tornkts.handlers import BaseHandler
from tornkts.handlers.object_handler import ObjectHandler


class BankExBaseHandler(BaseHandler):
    _payload = None

    def get_argument(self, name, default=BaseHandler._ARG_DEFAULT, strip=True, **kwargs):
        if self.request.method == 'POST':
            if self._payload is None:
                try:
                    self._payload = utils.json_loads(self.request.body)
                except:
                    pass
            if self._payload and name in self._payload:
                return self._payload[name]
            else:
                return super(BankExBaseHandler, self).get_argument(name, default, strip)
        else:
            return super(BankExBaseHandler, self).get_argument(name, default, strip)


class BankExObjectHandler(ObjectHandler):
    _payload = None

    def get_argument(self, name, default=BaseHandler._ARG_DEFAULT, strip=True, **kwargs):
        if self.request.method == 'POST':
            if self._payload is None:
                try:
                    self._payload = utils.json_loads(self.request.body)
                except:
                    pass
            if self._payload and name in self._payload:
                return self._payload[name]
            else:
                return super(BankExObjectHandler, self).get_argument(name, default, strip)
        else:
            return super(BankExObjectHandler, self).get_argument(name, default, strip)
