# coding=utf-8
from models.bankex import Admin
from tornkts.utils import PasswordHelper
from settings import options
from mongoengine import connection as mongo_connection
import getpass

__author__ = 'grigory51'

mongo_connection.connect(host=options.mongo_uri)

email_busy = 1
email = ''
while email_busy > 0:
    email = raw_input(u'Enter email: ')
    email_busy = Admin.objects(email=email).count()
    if email_busy > 0:
        print 'Email busy, try again'

password = getpass.getpass(u'Enter password: ')
name = raw_input(u'Enter name (optional): ')
try:
    name = name.decode('utf-8')
    email = email.decode('utf-8')
    password = password.decode('utf-8')

    admin = Admin(
            email=email,
            password=PasswordHelper.get_hash(password),
            name=name
    )
    admin.save()
    print 'Admin successfully added'
except Exception as e:
    print 'Admin not added'
    print e.message
