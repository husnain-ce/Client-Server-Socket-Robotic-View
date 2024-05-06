import multiprocessing as mp
import socket,os
from connection import conn

from util.display import *

if __name__ == '__main__':
    
    # host = '192.168.0.197'
    display_header()
    flag = main_panel()
    
    host = '127.0.0.1'
    port = 9999
    conn_obj = conn.CreateConnection(host,port)
    check = conn_obj.starting(flag)
    
    if check:
        conn_obj.conn_conntroler()
        
    else:
        print('Connection Close, Try Again')