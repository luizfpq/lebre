import random

def FirstName():
    lines = open('./assets/FirstName.txt').read().splitlines()
    myline = random.choice(lines)
    return myline
