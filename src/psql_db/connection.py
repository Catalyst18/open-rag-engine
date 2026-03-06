import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )