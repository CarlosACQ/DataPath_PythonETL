# sql-server (source db)
sqlserver_db_config ={
    'Trusted_Connection': 'yes',
    'driver': "{ODBC Driver 18 for SQL Server}",
    'server': 'localhost',
    'database': 'AdventureWorks2019',
    'user': 'etl',
    'password': 'etl123'
}


postgres_db_config ={
    'server': 'localhost',
    'database': 'AdventureWorks',
    'user': 'etl',
    'password': 'etl123',
    'port':'5432'
}

