# Lebre populator
A Database Populator is a tool which helps you to populate your projects' database tables with randomly generated content. With this tool you no longer need to write queries or to compile forms by yourself wasting a lot of time before to start to work on your applications.

## Why Lebre?

Lebres (Hares in english) are animals that usually represent fertility, they are related to several folk manifestations, therefore, there is nothing more fair to populate your database than our Lebre.

# Using Lebre

Inside the "table" folder create the json files and name them as the tables names ex: 

    Table username → username.json
    Table employee → employee.json


Filling in the json files:

    {
		"FieldName": "Nome", 
		"DataType": "varchar",
		"Length": "56",
		"StringType": "FirstName",
		"RecordsToGenerate": "171"
	}

    FieldName, DataType and Length are atributes inherited from table atributes, so just copy from them.

    StringType is a set of data wich we'll put on these fields:

    Varchar:
        Address
        CityName
        StateProvince
        Country
        Email
        FirstName
        LastName
        FullName
    Char
    Text    
    Int
    Float
    Bit
    Boolean
    Date
    Datetime
    Timestamp
    Time
    Year

    #Depends
        Python 3.7