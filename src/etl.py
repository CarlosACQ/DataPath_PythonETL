import pandas as pd

def extract_customers(connection):
    #Traer los datos de Cliente y arreglar el tipo de dato
    query_customers = "SELECT CustomerId, PersonId, StoreId, TerritoryID, AccountNumber FROM [Sales].[Customer]"
    df_customers = pd.read_sql(query_customers, connection)
    return df_customers

def extract_person(connection):
    #Traer los datos de Persona
    query_person = "SELECT BusinessEntityID AS PersonId, PersonType, FirstName, LastName FROM [Person].[Person]"
    df_person = pd.read_sql(query_person, connection)
    return  df_person


def extract_address(connection):
    #Traer los datos de Dirección
    query_address = "SELECT BusinessEntityID AS PersonId, AddressLine1, City, PostalCode FROM [Person].[BusinessEntityAddress] AS BA INNER JOIN [Person].[Address] A ON A.AddressID = Ba.AddressID"
    df_address = pd.read_sql(query_address, connection)
    return df_address


def transform_data(df_customers:pd.DataFrame, df_person:pd.DataFrame, df_address:pd.DataFrame):
    #Seleccionar columnas necesarias
    df_customers = df_customers.loc[:,['CustomerId','PersonId','StoreId','AccountNumber']]

    #Cambiar tipo de dato
    df_customers[['PersonId','StoreId']] = df_customers[['PersonId','StoreId']].apply(lambda x : x.astype(pd.Int64Dtype()))
    df_person["PersonId"] = df_person["PersonId"].astype(pd.Int64Dtype())

    #Cruzar clientes con personas y limpiar los clientes que no esten registrados con datos de persona
    df_customer_person = df_customers.merge(df_person, on='PersonId', how='inner')

    #Agregar datos de dirección --opcional si la encuentra
    df_customer_address = df_customer_person.merge(df_address, on='PersonId', how='left')

    #Cantidad de personas por ciudad
    df_adress_count_by_person = df_customer_address.groupby('City')['City'].count().reset_index(name='count')
    
    #Filtrar clientes que viven en ciudades con mas de 100 clientes-personas
    df_top_cities = df_adress_count_by_person['count'] > 100
    df_customers_top_cities = df_adress_count_by_person[df_top_cities]
    df_customer_dim = df_customer_address[df_customer_address['City'].isin(df_customers_top_cities['City'])]
    return df_customer_dim

def load_data_destination(df_customer:pd.DataFrame, engine):
    df_customer.to_sql('DimTopCustomers',engine,if_exists='replace',index=False)
    print(f'Se registraron {len(df_customer.index)} filas')
