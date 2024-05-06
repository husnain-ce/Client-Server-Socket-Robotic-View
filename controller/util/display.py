from colored import fg, attr
import random


def display_header():

    """ Display the ascii header """

    draw = """
    {}       
    {}  The Socket Management System ( Client-Server Model )
    {}  - Yasir
    {}
    {} /!\\ To Operate with E2EE layer /!\\
    {}
    {}"""
    lines = len(draw.splitlines())
    mini = 0
    maxi = 255 - (lines + 1)
    rand_min = random.randint(mini, maxi)
    formater = [fg(color) for color in range(rand_min, rand_min + (lines - 2))] + [attr('reset')]
    draw = draw.format(*formater)
    print(draw)

def main_panel():
    print('--------------------------------------')
    try:
        while True:
            print('1: Sign-Up >> ') 
            print('2: Sign-In >> ')
            check = int(input('>> '))
            
            if check == 1:
                print('--------------------------------------')
                return 'sign_up'

            elif check == 2:
                print('--------------------------------------')
                return 'sign_in'

    except Exception as e:
        print('Please Enter Valid Input', e)

    