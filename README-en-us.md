# Lebre Populator
A Database Populator is a tool that helps you fill the tables of your database projects with randomly generated content. With this tool, you no longer need to write inserts or fill out forms, saving a lot of time before you start working on your applications.

#### Why Lebre?
Lebres (Hares) are animals that often represent fertility, and they are related to various popular manifestations. Therefore, nothing is more suitable for populating your database than our Lebre.

## Using Lebre

If you are on Linux:

    ./main.py

If you are a Windows user:

    python main.py

If you are a Mac User:

    # Buy a coffee, you've got the money;
    python main.py

Inside the "table" folder, create JSON files and name them with a numerical sequence so they are created in the order of interdependence, according to the following suggestion:
example:

    Table employee → 00_employee.json
    Table username → 01_username.json

Filling out the JSON files:

    {
        "TableName": "tbl_name",
        "FieldList": "fieldName0, fieldName1, fieldName2, fieldName3, fieldName4",
        "DataType": "CPF,FullName,Varchar,Date,CPF",
        "RecordsToGenerate": 100
    }

- For "TableName", the name of the table where the inserts will occur.

- For "FieldList", the names of the fields are attributes inherited from the table's attributes, so copy their names exactly as they are in the table.

- For "DataType", just look at the list of data types below and relate them to your fields so that the chosen data is compatible with the field's filling in the tuple.

- In "RecordsToGenerate", define an integer number to set the number of inserts to be made.

## Available Data Types
Data types are a set of data that we will place in the table fields. Our code will find the data and define it based on a type defined by one of these:

#### Primitive Types
    Serial
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
    Address → Address type, does not include a number, just type of address and random name
    CityName → Random city name, independent of state <Interdependence will be implemented, city - state and country>
    StateProvince → State name independent of city or country <Interdependence will be implemented, city - state and country>
    Country → Country name <Interdependence will be implemented, city - state and country>
    Email → Random email name implemented in the format name.surname@server.address
    FirstName → First name
    LastName → Last name
    FullName → Full name
    CPF → Individual Taxpayer Registry
    Sex → Gender, can be customized according to the reference in the DataLoader file

## Dependencies
    Python 3.7+