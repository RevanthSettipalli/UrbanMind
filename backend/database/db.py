import psycopg2

def get_connection():
    return psycopg2.connect(
        host="urbanmind-postgres",
        database="urbanmind",
        user="admin",
        password="admin123",
        port="5432"
    )