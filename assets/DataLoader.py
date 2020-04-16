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
        return random.randint(0, 999999)
    if dType == 'CPF':
        return random.randint(10000000000, 99999999999)
    # Use: Varchar:size
    if "Varchar" in dType:
        return random_char(int(dType.split(":")[1])).upper()
    if dType == 'Date':
        return random_date("1/1/1970", "1/1/2000", random.random())
    


    # Set a default dataType, wich returns itself, to set default values on fields 
    # Model 
    #      Default:'00235'
    # Return: '00235'
    # Model 
    #      Default:00235
    # Return: 00235
    
    if "Default" in dType:
        return dType.split(":")[1]