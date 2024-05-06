from colored import fg, attr
import random

def display_header():

    """ Display the ascii header """

    draw = """
    {}       
    {}  ___________    .__           _________                                        
    {}  \__    ___/___ |  |   ____  /   _____/__ _________  ____   ___________ ___.__.
    {}    |    |_/ __ \|  | _/ __ \ \_____  \|  |  \_  __ \/ ___\_/ __ \_  __ <   |  |
    {}    |    |\  ___/|  |_\  ___/ /        \  |  /|  | \/ /_/  >  ___/|  | \/\___  |
    {}    |____| \___  >____/\___  >_______  /____/ |__|  \___  / \___  >__|   / ____|
    {}               \/          \/        \/            /_____/      \/       \/     
    {} 
    {}  The TeleSurgery ( Controller and Robot System  )
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