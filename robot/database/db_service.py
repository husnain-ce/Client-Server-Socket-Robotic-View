
import re
from unittest import result
import sys, os
# from mysql_conf import connection_pool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mysql_conf import connection_pool

def create_table():
    cursor = connection_pool.cursor()
        
    userRecord_ = """CREATE TABLE USERS (
                    id INT AUTO_INCREMENT,
                    NAME  VARCHAR(20) NOT NULL,
                    EMAIL VARCHAR(50),
                    PASSWD VARCHAR(50),
                    PRIMARY KEY(id)
                   );
                   """
 
    cursor.execute(userRecord_)
    
    userRecord = """CREATE TABLE MESSAGE (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    MESSAGE VARCHAR(200) NOT NULL,
                    IV VARCHAR(200) NOT NULL,
                    MSG_ID INT NOT NULL,
                    CONSTRAINT `FK_MSG_USERS`
                        FOREIGN KEY (MSG_ID) REFERENCES USERS (id)
                    );
                   """
    
 
    cursor.execute(userRecord)
    cursor.close()

def insert_table(info):
    cursor = connection_pool.cursor()
    statement = '''INSERT INTO USERS (NAME, EMAIL, PASSWD) 
                    VALUES (%s, %s, %s)'''
    cursor.execute(statement, info)
    
    connection_pool.commit()
    cursor.close()
    
def insert_msg(msg):
    cursor = connection_pool.cursor()
    statement = '''INSERT INTO MESSAGE (MESSAGE, IV, MSG_ID)
                    VALUES(%s, %s , %s);'''

    cursor.execute(statement, msg)
    connection_pool.commit()
    cursor.close()
    

def read_join_table():
    cursor = connection_pool.cursor()
    statement = '''SELECT USERS.id, USERS.name,USERS.email, USERS.passwd, MESSAGE.MESSAGE, 
                    MESSAGE.IV FROM USERS INNER JOIN MESSAGE ON USERS.id=MESSAGE.MSG_ID'''
    cursor.execute(statement)
    
    result = cursor.fetchall()
    cursor.close()

    return [{
    'id': id,
    'name': name,
    'email': email,
    'passwd': passwd,
    'message': message,
    'iv' : iv
    
    } for id, name, email, passwd, message, iv in result]


def read_table():
    cursor = connection_pool.cursor()
    statement = '''SELECT * from USERS'''
    cursor.execute(statement)
    
    result = cursor.fetchall()
    cursor.close()

    return [{
    'id': id,
    'name': name,
    'email': email,
    'passwd': passwd,
    
    } for id, name, email, passwd in result]


def delete_table():
    cursor = connection_pool.cursor()
    try:
        statement = 'Drop Table if exists USERS, MESSAGE'
        cursor.execute(statement)
        cursor.close()
        
    except:
        pass


