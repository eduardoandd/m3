# funcoes_clientes.py
from banco import conectar

def cadastrar_cliente(nome, cpf, telefone, email):
    conn = conectar()
    cursor = conn.cursor()

    # Verifica se CPF já existe
    query_check = "SELECT COUNT(*) FROM clientes WHERE cpf = %s"
    cursor.execute(query_check, (cpf,))
    (count,) = cursor.fetchone()

    if count > 0:
        cursor.close()
        conn.close()
        return False, "Cliente já cadastrado! Verifique os Dados."

    # Inserir novo cliente
    query_insert = "INSERT INTO clientes (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
    cursor.execute(query_insert, (nome, cpf, telefone, email))
    conn.commit()

    cursor.close()
    conn.close()
    # listar_clientes()

    return True, "Cliente cadastrado com sucesso!"


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nome, cpf, telefone, email FROM clientes")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def consultar_cliente_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    nome_pesquisa = f"%{nome}%"  # pesquisa LIKE com curinga
    query = "SELECT id_cliente, nome, cpf, telefone, email FROM clientes WHERE nome LIKE %s"
    cursor.execute(query, (nome_pesquisa,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def editar_cliente(id_cliente, nome, cpf, telefone, email):
    conn = conectar()
    cursor = conn.cursor()

    # Verificar se o CPF já está em uso por outro cliente
    query_check = "SELECT COUNT(*) FROM clientes WHERE cpf = %s AND id_cliente != %s"
    cursor.execute(query_check, (cpf, id_cliente))
    (count,) = cursor.fetchone()
    if count > 0:
        cursor.close()
        conn.close()
        return False, "CPF já está cadastrado para outro cliente!"

    query_update = """
        UPDATE clientes
        SET nome = %s, cpf = %s, telefone = %s, email = %s
        WHERE id_cliente = %s
    """
    cursor.execute(query_update, (nome, cpf, telefone, email, id_cliente))
    conn.commit()

    cursor.close()
    conn.close()

    return True, "Cliente atualizado com sucesso!"


def excluir_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    query_delete = "DELETE FROM clientes WHERE id_cliente = %s"
    cursor.execute(query_delete, (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Cliente excluído com sucesso!"
