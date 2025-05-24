# banco.py
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # colocar a senha aqui, se precisar
            database='locadora'
        )
        print(conexao)
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
