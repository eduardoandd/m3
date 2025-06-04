# funcoes_locacao.py
from banco import conectar
from datetime import datetime

# Lista de status válidos para validação
STATUS_VALIDOS = ["Pendente", "Ativa", "Concluída", "Cancelada"]

def cadastrar_locacao(id_cliente, id_veiculo, data_inicio, data_termino, valor, status):
    conn = conectar()
    cursor = conn.cursor()

    # Validação do status
    if status not in STATUS_VALIDOS:
        cursor.close()
        conn.close()
        return False, f"Status inválido! Escolha um dos status: {', '.join(STATUS_VALIDOS)}"
    
     # Converter de 'DD/MM/YYYY' para datetime.date
    try:
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_termino = datetime.strptime(data_termino, '%d/%m/%Y').date()
    except ValueError as e:
        cursor.close()
        conn.close()
        return False, f"Erro na conversão de data: {e}"

    # Inserir nova locação
    query_insert = """
        INSERT INTO locacoes (id_cliente, id_veiculo, data_inicio, data_termino, valor, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_insert, (id_cliente, id_veiculo, data_inicio, data_termino, valor, status))
    conn.commit()

    cursor.close()
    conn.close()

    return True, "Locação registrada com sucesso!"


def listar_locacoes():
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT l.id_locacao, c.nome AS cliente, v.modelo AS veiculo, 
               l.data_inicio, l.data_termino, l.valor, l.status
        FROM locacoes l
        JOIN clientes c ON l.id_cliente = c.id_cliente
        JOIN veiculos v ON l.id_veiculo = v.id_veiculo
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def consultar_locacao_por_cliente(nome_cliente):
    conn = conectar()
    cursor = conn.cursor()
    nome_pesquisa = f"%{nome_cliente}%"
    query = """
        SELECT l.id_locacao, c.nome AS cliente, v.modelo AS veiculo, 
               l.data_inicio, l.data_termino, l.valor, l.status
        FROM locacoes l
        JOIN clientes c ON l.id_cliente = c.id_cliente
        JOIN veiculos v ON l.id_veiculo = v.id_veiculo
        WHERE c.nome LIKE %s
    """
    cursor.execute(query, (nome_pesquisa,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def editar_locacao(id_locacao, id_cliente, id_veiculo, data_inicio, data_termino, valor, status):
    conn = conectar()
    cursor = conn.cursor()

    # Validação do status
    if status not in STATUS_VALIDOS:
        cursor.close()
        conn.close()
        return False, f"Status inválido! Escolha um dos status: {', '.join(STATUS_VALIDOS)}"

    query_update = """
        UPDATE locacoes
        SET id_cliente = %s,
            id_veiculo = %s,
            data_inicio = %s,
            data_termino = %s,
            valor = %s,
            status = %s
        WHERE id_locacao = %s
    """
    cursor.execute(query_update, (id_cliente, id_veiculo, data_inicio, data_termino, valor, status, id_locacao))
    conn.commit()

    cursor.close()
    conn.close()

    return True, "Locação atualizada com sucesso!"


def cancelar_locacao(id_locacao):
    conn = conectar()
    cursor = conn.cursor()

    # Atualizar status para 'Cancelada'
    query = "UPDATE locacoes SET status = 'Cancelada' WHERE id_locacao = %s"
    cursor.execute(query, (id_locacao,))
    conn.commit()

    cursor.close()
    conn.close()
    return True, "Locação cancelada com sucesso!"


def atualizar_status_locacao(id_locacao, novo_status):
    conn = conectar()
    cursor = conn.cursor()

    # Validação do novo status
    if novo_status not in STATUS_VALIDOS:
        cursor.close()
        conn.close()
        return False, f"Status inválido! Escolha um dos status: {', '.join(STATUS_VALIDOS)}"

    # Atualiza o status da locação
    query = "UPDATE locacoes SET status = %s WHERE id_locacao = %s"
    cursor.execute(query, (novo_status, id_locacao))
    conn.commit()

    cursor.close()
    conn.close()
    return True, "Status da locação atualizado com sucesso!"
