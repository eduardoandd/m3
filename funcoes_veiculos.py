# funcoes_veiculos.py
from banco import conectar


# Lista de tipos válidos para validação
TIPOS_VALIDOS = ["Sedan", "Hatch", "SUV", "Moto", "Van"]


def contar_veiculos_por_marca():
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT marca, COUNT(*) FROM veiculos GROUP BY marca"
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def cadastrar_veiculo(modelo, marca, cor, placa, tipo, ano):
    conn = conectar()
    cursor = conn.cursor()

    # Verifica se a placa já existe
    query_check = "SELECT COUNT(*) FROM veiculos WHERE placa = %s"
    cursor.execute(query_check, (placa,))
    (count,) = cursor.fetchone()

    if count > 0:
        cursor.close()
        conn.close()
        return False, "Veículo com essa placa já cadastrado! Verifique os Dados."

    # Validação do tipo
    if tipo not in TIPOS_VALIDOS:
        cursor.close()
        conn.close()
        return False, f"Tipo inválido! Escolha um dos tipos: {', '.join(TIPOS_VALIDOS)}"

    # Inserir novo veículo
    query_insert = """
        INSERT INTO veiculos (modelo, marca, cor, placa, tipo, ano)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_insert, (modelo, marca, cor, placa, tipo, ano))
    conn.commit()

    cursor.close()
    conn.close()

    return True, "Veículo cadastrado com sucesso!"


def listar_veiculos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_veiculo, modelo, marca, cor, placa, tipo, ano FROM veiculos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def consultar_veiculo_por_modelo(modelo):
    conn = conectar()
    cursor = conn.cursor()
    modelo_pesquisa = f"%{modelo}%"  # pesquisa LIKE com curinga
    query = """
        SELECT id_veiculo, modelo, marca, cor, placa, tipo, ano 
        FROM veiculos 
        WHERE modelo LIKE %s
    """
    cursor.execute(query, (modelo_pesquisa,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def editar_veiculo(id_veiculo, modelo, marca, cor, placa, tipo, ano):
    conn = conectar()
    cursor = conn.cursor()

    # Verificar se a placa já está em uso por outro veículo
    query_check = "SELECT COUNT(*) FROM veiculos WHERE placa = %s AND id_veiculo != %s"
    cursor.execute(query_check, (placa, id_veiculo))
    (count,) = cursor.fetchone()
    if count > 0:
        cursor.close()
        conn.close()
        return False, "Placa já está cadastrada para outro veículo!"

    # Validação do tipo
    if tipo not in TIPOS_VALIDOS:
        cursor.close()
        conn.close()
        return False, f"Tipo inválido! Escolha um dos tipos: {', '.join(TIPOS_VALIDOS)}"

    query_update = """
        UPDATE veiculos
        SET modelo = %s, marca = %s, cor = %s, placa = %s, tipo = %s, ano = %s
        WHERE id_veiculo = %s
    """
    cursor.execute(query_update, (modelo, marca, cor, placa, tipo, ano, id_veiculo))
    conn.commit()

    cursor.close()
    conn.close()

    return True, "Veículo atualizado com sucesso!"


def excluir_veiculo(id_veiculo):
    conn = conectar()
    cursor = conn.cursor()
    query_delete = "DELETE FROM veiculos WHERE id_veiculo = %s"
    cursor.execute(query_delete, (id_veiculo,))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Veículo excluído com sucesso!"
