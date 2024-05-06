
# importing required libraries
import mysql.connector
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import env

dataBase = mysql.connector.connect(
  user = os.environ['user'],
  passwd =os.environ['passwd'],
  host = '127.0.0.1',
  auth_plugin= 'mysql_native_password'
)
 
# preparing a cursor object
cursorObject = dataBase.cursor()

# creating database
cursorObject.execute("CREATE DATABASE secure_tele")
