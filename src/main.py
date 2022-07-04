from etl import *
import db


if __name__ == '__main__':
    # Conexión SOURCE
    try:
        connection = db.sqlserver_conection()
        print("Conexión exitosa.")
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
   
    # Extracción
    print("Empezando extracción de datos.")
    df_customers = extract_customers(connection)
    df_person = extract_person(connection)
    df_address = extract_address(connection)

    # Transformación
    print("Empezando transformación de datos.")
    df_dim_customer = transform_data(df_customers,df_person,df_address)

    # Carga
    postgres_connection = db.postgres_conection()
    load_data_destination(df_dim_customer, postgres_connection)