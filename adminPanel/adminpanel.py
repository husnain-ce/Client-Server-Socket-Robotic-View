from email import message
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot.database import db_service
from robot.connection import secure, conn
from controller.connection.secure import decrypt, _hash
import hashlib
import ast

result = db_service.read_join_table()

print('------------------------------------------------------------------------')

print("{:<15} {:<15} {:<15} {:<15} {:<15}".format('id', 'name', 'email','passwd','message'))

hash = str(_hash('message')).encode('utf-8')
key = hashlib.sha256(hash).digest()
msg_li, iv_li = [], []


def ast_decode(msg):
    msg = ast.literal_eval(msg)
    return msg.strip() 


for record in result:
    print("{:<15} {:<15} {:<15} {:<15} {:<15}".format(
                                                str(record['id']), 
                                                str(record['name']), 
                                                str(record['email']), 
                                                str(record['passwd']), 
                                                str(decrypt(
                                                    ast_decode(record['message']),
                                                            key,
                                                    ast_decode(record['iv']))).strip(),
                                                
                                                )
        )
    print('------------------------------------------------------------------------')
