
import mysql.connector
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import env

dbconfig = {
    'user': os.environ['user'],
    'passwd': os.environ['passwd'],
    'database': 'secure_tele',
}

connection_pool = mysql.connector.connect(
    pool_name='mypool',
    pool_size=3,
    **dbconfig)
