import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",     # docker-compose service name
        database="mydatabase",
        user="user",
        password="password",
        port=5432
    )
    return conn
