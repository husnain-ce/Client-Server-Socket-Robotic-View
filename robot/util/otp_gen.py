# import library
import math, random
# import smtplib
# import win32com.client
from util.env import config

# function to generate OTP
def generateOTP() :

	# Declare a digits variable
	# which stores all digits
	digits = "0123456789"
	OTP = ""

# length of password can be changed
# by changing value in range
	for i in range(6):
		OTP += digits[math.floor(random.random() * 10)]

	return OTP

def otp_email(OTP):
    otp = OTP + " is your OTP"

    
    # Dumy Concept of Otp
    with open('otp.txt', 'w') as file:
        file.write(otp)

    return otp

def send_mail(OTP):
    
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'contact@company.com'
    mail.Subject = 'OTP Authentication'
    mail.HTMLBody = '<h3>TeleSurguery</h3>'
    mail.Body = otp_email(OTP)
    mail.Save()
    mail.Send()

# if __name__ == "__main__":
#     opt = generateOTP()
#     send_mail(opt)