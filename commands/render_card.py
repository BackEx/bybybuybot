from tornado.httpclient import HTTPRequest, HTTPClient
from models.awa import Offer
from settings import options
import sys

from utils import gen_path, mkdir

if len(sys.argv) < 3:
    raise Exception('Enter MongoId')

try:
    offer = Offer.objects.get(id=sys.argv[2])
except Exception as e:
    raise e

url = 'http://3007.vkontraste.ru/?url=http://{0}/api/offers.html?id={1}'.format(options.server_name, offer.get_id())

client = HTTPClient()
req = HTTPRequest(url)
res = client.fetch(req)

path = gen_path()
mkdir(path.get('folder'))
with open(path.get('fullname'), "w") as f:
    f.write(res.body)

offer.rendered_img = path.get('relname')
offer.save()