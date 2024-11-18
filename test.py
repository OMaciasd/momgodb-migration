import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="example_user",
        password="example_password",
        dbname="example_db"
    )
    print("Conexión a PostgreSQL establecida con éxito.")
except Exception as e:
    print("Error al conectar a PostgreSQL:", e)
