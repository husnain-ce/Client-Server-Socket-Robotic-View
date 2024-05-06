import email
from email import message
import socket,os,sys,time,subprocess
from util import otp_gen
from util import env
from connection.secure import _hash, encrypt, decrypt 
import hashlib, ast
from database.db_service import *
from os import name as os_name

class CreateConnection:
    def __init__(self,host: str, port: str):
        self.host = host
        self.port = port
        self.socket = None
        self.otp = ''
        self.result = ''
        self.curr_uid = ''
        self.email_ = ''
        hash = str(_hash('message')).encode('utf-8')
        self.key = hashlib.sha256(hash).digest()
        self.conn_conntroler()
        
    def create_conn(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as message:
            print("socket error: %s" % message)
            sys.exit(1)
            
    def connect_socket(self):
        try:
            self.socket.connect((self.host, self.port))
        
        except socket.error as msg:
            print("Connection Error: %s" % msg)
            time.sleep(5)
            self.connect_socket()
            
    def ping_socket(self):
        try:
            self.socket.send(str("ping").encode('utf-8'))
       
        except socket.error as msg:
            print("Couldn't accept connection %s'",msg)
            
    def recv_email(self):
        try: 
            email = self.socket.recv(16384).decode('utf-8')
            password = self.socket.recv(16384).decode('utf-8')
            
            return email, password
                        
        except socket.error as msg:
            print("Couldn't recv commands'%s"%msg)
    
    def recv_commands(self):
        try: 
            recv_cmd = self.socket.recv(16384).decode('utf-8')
            return recv_cmd
                        
        except socket.error as msg:
            print("Couldn't recv commands'%s"%msg)
    
    def send_commands(self,commands):
        try:
            self.socket.send(str(commands).encode('utf-8'))
        except socket.error as msg:
            print("Couldn't send initial' %s"%msg)

    def enc_layer_proc(self, message):
        
        iv = os.urandom(16)
        enc_msg = encrypt(message, self.key, iv)
        
        return enc_msg, iv
    
    def dcryt_layer_proc(self, rcv_enc_msg):
        dec_msg = ''
        try:
            rcv_enc_msg = ast.literal_eval(rcv_enc_msg)
            
            enc_msg = rcv_enc_msg[0]
            iv = rcv_enc_msg[1]
            
            dec_msg = decrypt(enc_msg, self.key, iv).strip().decode('utf-8')
            
        except:
            pass
        
        return dec_msg
    
    def dcryt_layer_proc_mail(self, rcv_enc_msg):
        try:
            rcv_enc_msg = ast.literal_eval(rcv_enc_msg)
            
            enc_name = rcv_enc_msg[0]
            iv_name = rcv_enc_msg[1]
            
            enc_mail = rcv_enc_msg[2]
            iv_mail = rcv_enc_msg[3]
            
            enc_pass = rcv_enc_msg[4]
            iv_pass = rcv_enc_msg[5]
            

            name = decrypt(enc_name, self.key, iv_name).strip().decode('utf-8')
            email = decrypt(enc_mail, self.key, iv_mail).strip().decode('utf-8')
            passwd = decrypt(enc_pass, self.key, iv_pass).strip().decode('utf-8')
            
        except:
            pass
        
        return name, email, passwd
    
    def dcryt_layer_sign_mail(self, rcv_enc_msg):
        email, passwd = '', ''
        try:
            rcv_enc_msg = ast.literal_eval(rcv_enc_msg)
            
            enc_mail = rcv_enc_msg[0]
            iv_mail = rcv_enc_msg[1]
            
            enc_pass = rcv_enc_msg[2]
            iv_pass = rcv_enc_msg[3]
            
            email = decrypt(enc_mail, self.key, iv_mail).strip().decode('utf-8')
            passwd = decrypt(enc_pass, self.key, iv_pass).strip().decode('utf-8')
            
        except:
            pass
        
        return email, passwd
        
    def initial_phase(self):
        self.create_conn()
        self.connect_socket()
    
    def send_enc_message(self, message, callFrom = None):
        enc_message, iv = self.enc_layer_proc(message)
        self.send_commands( [enc_message,iv] )
        
        if callFrom == 'Chat':
            self.store_chat([enc_message, iv])
    
    def rcv_enc_message(self, callFrom=None):
        
        
        rcv_enc_msg = self.recv_commands()
        dec_msg = self.dcryt_layer_proc(rcv_enc_msg)
        
        if callFrom == 'Chat':
            self.store_chat(rcv_enc_msg)
        
        return dec_msg
    
    def sign_up(self):
        self.send_enc_message('Controller')
        enc_msg = self.recv_commands()
        name, email, passwd = self.dcryt_layer_proc_mail(enc_msg)
        
        print(f'inserting {name, email, passwd}')
        insert_table([name, email, passwd])
    
    def sign_in(self):
        self.send_enc_message('Sign_In')
        enc_msg = self.recv_commands()
        self.email_, passwd_ = self.dcryt_layer_sign_mail(enc_msg)
        
        print(self.email_, passwd_)
        
        self.result = read_table()
        
        for record in self.result:
            try:
                if record['email'] == self.email_ and record['passwd'] == passwd_:
                    self.curr_uid = record['id']
                    
                    print('Successfull logged in')
                    self.send_enc_message('SignInDone')
                    return True
            
            except Exception as e:
                print(e)

            else: pass
    
    def clear(self):
        # for windows
        if os_name == 'nt':
            _ = os.system('cls')

        # for mac and linux
        else:
            _ = os.system('clear')
    
    def authentication(self):
         
        self.otp = otp_gen.generateOTP()
        otp_gen.otp_email(self.otp)
        
        # otp_gen.send_mail(self.otp)
        self.send_enc_message('Established')
        
        # rcv Otp
        rcv_otp = self.rcv_enc_message()
        
        if rcv_otp == self.otp:
            self.send_enc_message('Success')
            return True

        else: return False
        
    def store_chat(self, rcv_enc_msg):
        rcv_enc_msg = ast.literal_eval(str(rcv_enc_msg))
        enc_msg = str(rcv_enc_msg[0])
        iv = str(rcv_enc_msg[1])
        
        insert_msg([enc_msg, iv, self.curr_uid])
    
    def conn_conntroler(self):

        self.initial_phase()
        self.sign_up()
        check = self.sign_in()
        
        if check:
            check_ = self.authentication()
        
        # The Encryption chat layer proper
            if check_:
                self.clear()

                while True:
                    try:
                        # recv 
                        dec_msg = self.rcv_enc_message('Chat')
                        print(dec_msg)
                        
                        #send
                        commands = input('>> Enter Commands..: ')
                        self.send_enc_message(commands, 'Chat')
                        
                    except Exception as e:
                        print("Error on socket connections: %s" %str(e))
            
    # else: print('Authenication Failed Try Again')
        
      