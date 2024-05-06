
from connection import conn
from util.display import display_header 


if __name__ == '__main__':

        # host = 'ip_addr_v4'
        display_header()
        host = '127.0.0.1'
        port = 9999
        conn.CreateConnection(host, port)

