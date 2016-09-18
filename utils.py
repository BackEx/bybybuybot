from datetime import datetime
from tornkts import utils
from settings import options
import hashlib


def mkdir(path):
    utils.mkdir(path)


def gen_path():
    hash = hashlib.md5(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')).hexdigest()
    result = {
        'folder': '%s/%s/%s' % (options.upload_path, hash[0:2], hash[2:4]),
        'filename': hash + '.png'
    }
    result.update({
        'fullname': '%s/%s' % (result.get('folder'), result.get('filename')),
        'relname': '%s/%s/%s.png' % (hash[0:2], hash[2:4], hash)
    })
    return result
