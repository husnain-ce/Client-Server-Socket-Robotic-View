
import socket ,os ,sys ,time
from os import name as os_name
from util import rejex_validation
import getpass
from connection.secure import _hash, encrypt, decrypt
import hashlib
import ast

class CreateConnection:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket = None
        self.conn = None
        hash = str(_hash('message')).encode('utf-8')
        self.key = hashlib.sha256(hash).digest()
        
    def create_conn(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as message:
            print("socket error: %s" % message)
            self.socket.close()
            sys.exit(1)
            
    def bind_socket(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
        except socket.error as msg:
            print("Couldn't bind socket %s"%msg)
            time.sleep(5)
            self.bind_socket()
            
    def accept_connection(self):
        try:
            self.conn,self.addr = self.socket.accept()
            print(f'Connection Initiated to ---> {self.addr}')
        except socket.error as msg:
            print("Couldn't accept connection %s'"%msg)
            self.socket.close()
    
    def recv_command(self):
        try:
            message = self.conn.recv(1024).decode('utf-8')
            return message
            
        except socket.error as msg:
            print("Couldn't recv socket' %s'"%msg)
            self.socket.close()
    
    def send_verification(self,email, password):
        try:
            self.conn.send(str(email).encode('utf-8'))
            self.conn.send(str(password).encode('utf-8'))
            
        except socket.error as msg:
            print("Couldn't send message ' %s'"%msg)
            self.socket.close()
            
    def send_commands(self,commands):
        try:
            self.conn.send(str(commands).encode('utf-8'))
            
        except socket.error as msg:
            print("Couldn't send message ' %s'"%msg)
            
    def socket_gethostname(self):
        try:
            return self.conn.recv(1024).decode('utf-8')
        except socket.error as msg:
            print("Couldn't send initial' %s"%msg)
            
    def recv_initial_info(self):
        try:
            return self.conn.recv(16384).decode('utf-8')
        except socket.error as msg:
            print("Couldn't send initial' %s"%msg)
    
    def enc_layer_proc(self, message):
        
        iv = os.urandom(16)
        enc_msg = encrypt(message, self.key, iv)
        
        return enc_msg, iv
    
    def dcryt_layer_proc(self, rcv_enc_msg):
        dec_msg = b''
        try:
            rcv_enc_msg = ast.literal_eval(rcv_enc_msg)
            
            enc_msg = rcv_enc_msg[0]
            iv = rcv_enc_msg[1]
            
            dec_msg = decrypt(enc_msg, self.key, iv).strip()
        except:
            pass
        
        return dec_msg.decode('utf-8')

    def proc_message(self, message):

        # SignUp Case
        if message == 'Controller':
                email, password, name = '','', ''

                while True:
                    name = input('Enter yours Name-->> ')
                    email = input(f'Enter yours Email->> ')

                    if rejex_validation.check(email):
                        password = getpass.getpass(prompt='Enter yours Password->> ')
                        return name, email, password                        
                    
                    else: print('Enter Correct Email e.g: user213@gmail.com')
        
        elif message == 'Sign_In':
            while True:
                    email = input(f'Enter yours Email->> ')

                    if rejex_validation.check(email):
                        password = getpass.getpass(prompt='Enter yours Password->> ')
                        return email, password                        
                    
                    else: print('Enter Correct Email e.g: user213@gmail.com')
                
        
        elif message == 'Established':
            while True:
                otp = input(f'Please Enter yours OTP sended on email: ')
                if otp:
                    return otp
                else: print('Please enter yours OTP')

        elif message == 'Success':
            return message
        
        else: return message
    
    def initial_phase_conn(self):
        self.create_conn()
        self.bind_socket()
        self.accept_connection() 
    
    def send_enc_message(self, message):
        enc_message, iv = self.enc_layer_proc(message)
        self.send_commands( [enc_message,iv] )
    
    def rcv_enc_message(self):
        rcv_enc_msg = self.recv_command()
        dec_msg = self.dcryt_layer_proc(rcv_enc_msg)
        
        return dec_msg
    
    def sign_up(self):
        dec_msg = self.rcv_enc_message()
        
        name, email, password = self.proc_message(dec_msg)
        
        enc_name, iv_name = self.enc_layer_proc(name)
        enc_mail, iv_mail = self.enc_layer_proc(email)
        enc_pass, iv_pass = self.enc_layer_proc(password)
        
        self.send_commands( [enc_name, iv_name 
                             ,enc_mail, iv_mail,
                             enc_pass, iv_pass] )
    
    def sign_in(self):
        dec_meg = self.rcv_enc_message()
        
        if dec_meg:
            
            email, passwd = self.proc_message(dec_meg)
            
            enc_mail, iv_mail = self.enc_layer_proc(email)
            enc_pass, iv_pass = self.enc_layer_proc(passwd)
            
            self.send_commands( [enc_mail, iv_mail,
                                enc_pass, iv_pass] )
            
            
            dec_msg = self.rcv_enc_message()
            if dec_msg == 'SignInDone':
                return True
            
            else: return False
        
    def authentication(self):
        
        # Otp recv
        dec_meg = self.rcv_enc_message()
        print(dec_meg)
        
        otp = self.proc_message(dec_meg)
        print(otp)
        
        self.send_enc_message(otp)
        
        # Verification
        dec_meg = self.rcv_enc_message()
        print(dec_meg)
        
        success = self.proc_message(dec_meg)
        return success
    
    def test(self):
        
        dec_msg = self.rcv_enc_message()
        
        name, email, password = self.proc_message(dec_msg)
        
        enc_name, iv_name = self.enc_layer_proc(name)
        enc_mail, iv_mail = self.enc_layer_proc(email)
        enc_pass, iv_pass = self.enc_layer_proc(password)
        
        self.send_commands( [enc_name, iv_name 
                             ,enc_mail, iv_mail,
                             enc_pass, iv_pass] )
        
    def starting(self, flag : str):
        self.initial_phase_conn()
        if flag == 'sign_up':
            self.sign_up()
            print('**** Successfully Sign-Up Now Please Enter to Login ****')
            check = self.sign_in()
            
            return check
        
        elif flag == "sign_in":
            check = self.sign_in()
            return check

        else:
            print('Please Enter Valid Input....')
    
    def clear(self):
        # for windows
        if os_name == 'nt':
            _ = os.system('cls')

        # for mac and linux
        else:
            _ = os.system('clear')
    
    def conn_conntroler(self):
       
        msg = self.authentication()
        
        # #create the encryption layer proper
        print('---------------------------------')
        if msg:
            self.clear()
            while True:
                try:
                    #send
                    commands = input('>> Enter Commands..: ')
                    self.send_enc_message(commands)
                    
                    # recv 
                    dec_msg = self.rcv_enc_message()
                    print(dec_msg)
                    
                except Exception as e:
                    print("Error on socket connections %s" %str(e))        
        
        print('---------------------------------')
