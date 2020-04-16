# Lebre populator
Um Database Populator é uma ferramenta que te ajuda preencher as tabelas de banco de dados dos seus projetos com conteúdo gerado aleatoriamente. Com essa ferramenta, você não precisa mais escrever inserts ou compilar formulários, perdendo muito tempo antes para começar a trabalhar em seus aplicativos.

#### Por que Lebre?
Lebres são animais que geralmente representam fertilidade, eles estão relacionados a várias manifestações populares, portanto, nada mais adequado para preencher seu banco de dados do que a nossa Lebre.


## Usando o Lebre

Se estiver no Linux:

    ./run.py

Se for usuário do Windows:

    python run.py

Se você for um Mac User:

    #Pague um cafezinho, 'cê' tem grana;
    python run.py

Dentro da pasta "table", crie os arquivos json e nomeie-os como nomes das tabelas
ex:

    Tabela username → username.json
    Tabela employee → employee.json


Preenchendo os arquivos JSON:

    {
		"FieldList": "fieldName0, fieldName1, fieldName2, fieldName3, fieldName4",
		"DataType": "CPF,FullName,Varchar,Date,CPF",
		"RecordsToGenerate": 100
	}

 - Para o "FieldList" os nomes dos arquivos são atributos herdados dos atributos da tabela, então copie os nomes deles, exatamente como estão na tabela.

 - Para o "DataType" basta olhar a lista de tipos de dados abaixo e relacioná-los com seus campos, de forma que o dado escolhido seja compatível com o preenchimento do campo na tupla.

 - Em "RecordsToGenerate" defina um número inteiro para definir o número de inserções a serem feitas.

## Data Types (Tipos de Dados) disponíveis
Tipos de dados é um conjunto de dados que colocaremos nos campos da tabela, nosso código encontrará os dados e os definirá com base em um tipo definido por um desses:

 #### Tipos Primitivos
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

 #### Tipos Complexos
    Address
    CityName
    StateProvince
    Country
    Email
    FirstName
    LastName
    FullName
    CPF


## Dependências
        Python 3.7
