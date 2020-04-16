# Lebre populator
A Database Populator is a tool which helps you to populate your projects' database tables with randomly generated content. With this tool you no longer need to write queries or to compile forms by yourself wasting a lot of time before to start to work on your applications.

#### Why Lebre?

Lebres (Hares in english) are animals that usually represent fertility, they are related to several folk manifestations, therefore, there is nothing more fair to populate your database than our Lebre.

## Using Lebre

If you are using Linux:

    ./run.py
if you are in Windows:

    python run.py
If you are a mac user:

    #Pay me some coffee, you've money;
    python run.py

Inside the "table" folder create the json files and name them as the tables names ex: 

    Table username → username.json
    Table employee → employee.json


Filling in the json files:

    {
		"FieldList": "fieldName0, fieldName1, fieldName2, fieldName3, fieldName4",
		"DataType": "CPF,FullName,Varchar,Date,CPF",
		"RecordsToGenerate": 100
	}

 - For "FieldList" the fieldNames are atributes inherited from table atributes, so just copy from them.

 - For "DataType"  just look the data types list below, and relate them with your fields.

 - In "RecordsToGenerate" set an integer to define the number of inserts to make.

## Disponible Data Types
Data Types is a set of data which we'll put on table fields, our code will find the data and set it based on a type set by one of those:

 #### Raw Types
    Varchar
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

 #### Complex Types
    Address
    CityName
    StateProvince
    Country
    Email
    FirstName
    LastName
    FullName
    CPF
    

## Depends
        Python 3.7
        
