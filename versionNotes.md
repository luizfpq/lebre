# v0.2.0
- altera a estrutura de diretórios migrando os tipos de dados para o diretório generators;

- Aperfeiçoa os tipos de dados numéricos separando-os em um generator;

- Adiciona interdependências entre as tabelas geradas e campos, por exemplo, na versão anterior um nome completo e a inicial do usuário poderiam ser diferentes, cada dado era gerado independente, ou seja, uma iteração era chamada e respondia para cada campo da tabela, sendo que as funções não recebiam parâmetros e devolviam dados aleatórios dentro dessas iterações, um campo 'FirstName' poderia ser Luiz e a inicial 'D', isso foi resolvido passando para as funções parâmetros sobre quantos campos devolver e as funções já devolvem um dicionario com a quantidade de dados necessária para a iteração que gerará cada insert, sendo assim, pode-se por exemplo criar um tipo de dado usuario, que recebe os tres primeiros caracteres do nome completo do dado tipo FullName ou FirstName+LastName.

# v2.0.0
- Aperfeiçoa a estrutura de diretórios, criando a pasta de saida(results) e padronizando a nomenclatura dos resultados em .sql
- Aperfeiçoa os tipos de dados relacionados a nomes, email e usernames para que haja consistencia nos dados
- Adiciona o gerador de tabelas (tables_generator.py)
- Adiciona menu de seleção
- Remove FirstNames.txt e LastNames.txt do datasources, implementando apenas o FullNames para melhorar a compatibilidade de nomes e diminuir o espaço em disco do repositório
  
# v2.0.1
- Adiciona normalizer.py para permitir a normalização dos arquivos datasources, até o momento permitindo apenas uppercase e lowercase;
- remove funções de normalização de dentro dos generators para melhorar o processamento, mantidos apenas lower do email e usernames;
