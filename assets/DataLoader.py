import random
from assets.Name import *
from assets.Varchar import *
from assets.DateTime import *

def DataLoad( dType ):
    if dType == 'FirstName':
        return  FirstName()
    if dType == 'LastName':
        return  LastName()
    if dType == 'FullName':
        return  FullName()
    if dType == 'Integer':
        return random.randint(0, 99999999999)
    if dType == 'CPF':
        return random.randint(10000000000, 99999999999)
    #@todo: varchar size
    if dType == 'Varchar':
        return random_char(3)
    if dType == 'Date':
        return random_date("1/1/1970", "1/1/2000", random.random())