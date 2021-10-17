from pony.orm import *

db = pony.orm.Database()

db.bind('mysql', host='127.0.0.1', user='root', passwd='', db='mystery')

