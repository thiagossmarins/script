import psycopg2;
from psycopg2 import extensions;

try:
    conn = psycopg2.connect(
        dbname="rickandmorty",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    
    if conn.status == extensions.STATUS_READY:
        print("Conexão bem sucedida")
    
    conn.close()

except psycopg2.Error as e:
    print("Erro na conexão:", e)