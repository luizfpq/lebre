import random

def FirstName():
    lines = open('./assets/FirstName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    return myline
def LastName():
    lines = open('./assets/LastName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    return myline
def FullName():
    lines = open('./assets/FirstName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    lines = open('./assets/LastName.txt').read().splitlines()
    myline = myline + ' ' + random.choice(lines)
    myline = myline.split(",")[0]
    return myline