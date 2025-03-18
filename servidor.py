import flask
from flask import Flask, request, jsonify
import sqlite3 

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("seu_banco_de_dados.db")

@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()

    imoveis = [
        {
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
        for row in rows
    ]
    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/<int:id>", methods=["GET"])
def get_imoveis_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = ?", (id,))
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
    return jsonify(imovel)

@app.route("/imoveis", methods=["POST"])
def add_imoveis():
    dados = request.json 
    required_fields = ["logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"]
    if not all(field in dados for field in required_fields):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"], dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"])
        )
        return jsonify({"message": "Imóvel adicionado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/imoveis/<int:id>/update", methods=["PUT"])
def update_imoveis(id):
    dados = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE imoveis
        SET logradouro = ?, tipo_logradouro = ?, bairro = ?, cidade = ?, cep = ?, tipo = ?, valor = ?, data_aquisicao = ?
        WHERE id = ?
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
    cursor.execute("SELECT * FROM imoveis WHERE id = ?", (id,))
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
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imoveis WHERE id = ?", (id,))
        imovel = cursor.fetchone()

        if not imovel:
            return jsonify({"error": "Imóvel não encontrado"}), 404

        cursor.execute("DELETE FROM imoveis WHERE id = ?", (id,))

    return jsonify({"message": "Imóvel deletado com sucesso!"}), 200

@app.route("/imoveis/tipo", methods=["GET"])
def get_imoveis_tipo():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()


    imoveis = [
        {
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": row[7],
            "data_aquisicao": row[8]
        }
        for row in rows
    ]

    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def get_imoveis_cidade(cidade):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade = ?", (cidade,))
    rows = cursor.fetchall()
    imoveis = []
    for row in rows:
        imoveis.append(
            {
                "id": row[0],
                "logradouro": row[1],
                "tipo_logradouro": row[2],
                "bairro": row[3],
                "cidade": row[4],
                "cep": row[5],
                "tipo": row[6],
                "valor": row[7],
                "data_aquisicao": row[8]
            }
        )
    return jsonify({"imoveis": imoveis})


if __name__ == "__main__":
    app.run(debug=True)