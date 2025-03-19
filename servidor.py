import flask
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mysql.connector
import os
import sqlite3 

app = Flask(__name__)

def connect_db():
    conn = mysql.connector.connect(**config)
    return conn

# dado do awein
load_dotenv('.env')


config = {
    "user": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "database": os.getenv("DATABASE"),
    "ssl_ca": os.getenv("SSL"),
}

@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()
    conn.close()
    imoveis_completo = []

    for imovel in imoveis:
        imoveis_completo.append(
            {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": float(imovel[7]),  # Certifica que "valor" seja float
                "data_aquisicao": str(imovel[8]),  # Certifica que "data" seja string
            }
        )

    return jsonify({"imoveis": imoveis_completo})


@app.route("/imoveis/<int:id>", methods=["GET"])
def get_imoveis_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM imoveis WHERE id = {id}")
    imovel = cursor.fetchone()
    conn.close()
    if imovel is None:
        return jsonify({"error": "Imóvel não encontrado"}), 404


    imovel = {
        "id": imovel[0],
        "logradouro": imovel[1],
        "tipo_logradouro": imovel[2],
        "bairro": imovel[3],
        "cidade": imovel[4],
        "cep": imovel[5],
        "tipo": imovel[6],
        "valor": imovel[7],
        "data_aquisicao": imovel[8],
    }
    return jsonify(imovel)


@app.route("/imoveis", methods=["POST"])
def add_imoveis():
    data = request.json 
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (data["logradouro"], data["tipo_logradouro"], data["bairro"], data["cidade"], data["cep"], data["tipo"], data["valor"], data["data_aquisicao"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Imóvel adicionado com sucesso!"}), 201


@app.route("/imoveis/<int:id>/update", methods=["PUT"])
def update_imoveis(id):
    dados = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        UPDATE imoveis
        SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
        WHERE id = %s
        """,
        (
            dados["logradouro"],
            dados["tipo_logradouro"],
            dados["bairro"],
            dados["cidade"],
            dados["cep"],
            dados["tipo"],
            dados["valor"],
            dados["data_aquisicao"],
            id,
        ),
    )
    conn.commit()
    cursor.execute(f"SELECT * FROM imoveis WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "Imóvel não encontrado"}), 404
    

    imovel = {
        "id": row[0],
        "logradouro": row[1],
        "tipo_logradouro": row[2],
        "bairro": row[3],
        "cidade": row[4],
        "cep": row[5],
        "tipo": row[6],
        "valor": row[7],
        "data_aquisicao": row[8],
    }
    return jsonify(imovel), 200


@app.route("/imoveis/<int:id>/delete", methods=["DELETE"])
def delete_imoveis(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM imoveis WHERE id = {id}")
    imovel = cursor.fetchone()

    if not imovel:
        return jsonify({"error": "Imóvel não encontrado"}), 404

    cursor.execute(f"DELETE FROM imoveis WHERE id = {id}",)
    conn.commit()

    return jsonify({"message": "Imóvel deletado com sucesso!"}), 200


@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def get_imoveis_tipo(tipo):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    imoveis = cursor.fetchall()
    imoveis_final = []
    conn.close()

    for imovel in imoveis:
        imoveis_final.append(
            {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
            })

    return jsonify({"imoveis": imoveis_final})


@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def get_imoveis_cidade(cidade):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    imoveis = cursor.fetchall()
    imoveis_final = []
    conn.close()

    for imovel in imoveis:
        imoveis_final.append(
            {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
            })

    return jsonify({"imoveis": imoveis_final})


if __name__ == "__main__":
    app.run(debug=True)