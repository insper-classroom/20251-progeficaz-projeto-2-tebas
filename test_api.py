import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db  # Importamos a aplicação Flask e a função de conexão


@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.connect_db")
def test_get_imoveis(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    
    mock_conn.cursor.return_value = mock_cursor

    # Retorno banco de dados com todos os imoveis
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get("/imoveis")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": [
            {'id': 1, "logradouro": 'Nicole Common', "tipo_logradouro": "Travessa", "bairro": "Lake Danielle", "cidade": "Judymouth", "cep": "85184", "tipo": "casa em condominio", "valor": 488423.52, "data_aquisicao": "2017-07-29"},
            {'id': 2, "logradouro": 'Price Prairie', "tipo_logradouro": "Travessa", "bairro": "Colonton", "cidade": "North Garyville", "cep": "93354", "tipo": "casa em condominio", "valor": 260069.89, "data_aquisicao": "2021-11-30"},
        ]
    }
    assert response.get_json() == expected_response




@patch("servidor.connect_db")
def test_get_imoveis_id(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    
    mock_cursor.fetchone.return_value = (
        1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184',
        'casa em condominio', 488423.52, '2017-07-29'
    )

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/1")
    assert response.status_code == 200

    expected_response = {
        "id": 1,
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 488423.52,
        "data_aquisicao": "2017-07-29"
    }

    assert response.get_json() == expected_response




@patch("servidor.connect_db")
def test_add_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    imovel = {
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "00184",
        "tipo": "casa em condominio",
        "valor": 488423.52,
        "data_aquisicao": "2017-07-29"
    }
    response = client.post("/imoveis", json=imovel)
    assert response.status_code == 201
    expected_response = {"message": "Imóvel adicionado com sucesso!"}
    assert response.get_json() == expected_response



@patch("servidor.connect_db")
def test_update_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, 'Nicole Common', 'Rua', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'
    )
    mock_connect_db.return_value = mock_conn
    dados = {
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Rua",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 488423.52,
        "data_aquisicao": "2017-07-29"
    }
    response = client.put("/imoveis/1/update", json=dados)
    assert response.status_code == 200
    expected_response = {
        "id": 1,
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Rua",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 488423.52,
        "data_aquisicao": "2017-07-29",
    }
    assert response.get_json() == expected_response




@patch("servidor.connect_db")
def test_delete_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'
    )

    mock_connect_db.return_value = mock_conn
    response = client.delete("/imoveis/1/delete")
    assert response.status_code == 200

    expected_response = {"message": "Imóvel deletado com sucesso!"}
    assert response.get_json() == expected_response




@patch("servidor.connect_db")
def test_get_imoveis_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (8, 'Richard Light', 'Travessa', 'New Rebeccaview', 'Benjaminberg', '64598', 'terreno', 684707.4, '2022-10-27')
    ]

    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/tipo")
    assert response.status_code == 200
    
    expected_response = {
        "imoveis": [
            {'id': 1, "logradouro": 'Nicole Common', "tipo_logradouro": "Travessa", "bairro": "Lake Danielle", "cidade": "Judymouth", "cep": "85184", "tipo": "casa em condominio", "valor": 488423.52, "data_aquisicao": "2017-07-29"},
            {'id': 8, "logradouro": 'Richard Light', "tipo_logradouro": "Travessa", "bairro": "New Rebeccaview", "cidade": "Benjaminberg", "cep": "64598", "tipo": "terreno", "valor": 684707.4, "data_aquisicao": "2022-10-27"},
        ]
    }
    assert response.get_json() == expected_response




@patch("servidor.connect_db")
def test_get_imoveis_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        # (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (6, 'Preston Terrace', 'Rua', 'North Lindseyview', 'Lake Michael', '99549', 'terreno', 946804.25, '2023-12-13'),
        # (8, 'Richard Light', 'Travessa', 'New Rebeccaview', 'Benjaminberg', '64598', 'terreno', 684707.4, '2022-10-27'),
        (50, 'Lori Summit', 'Travessa', 'Kristaside', 'Lake Michael', '24473', 'casa', 498926.13, '2019-02-27')
    ]

    mock_connect_db.return_value = mock_conn
    #%20 é o espaço em URL
    response = client.get("/imoveis/cidade/Lake%20Michael")
    assert response.status_code == 200
    
    expected_response = {
        "imoveis": [
            {'id': 6, "logradouro": 'Preston Terrace', "tipo_logradouro": "Rua", "bairro": "North Lindseyview", "cidade": "Lake Michael", "cep": "99549", "tipo": "terreno", "valor": 946804.25, "data_aquisicao": "2023-12-13"},
            {'id': 50, "logradouro": 'Lori Summit', "tipo_logradouro": "Travessa", "bairro": "Kristaside", "cidade": "Lake Michael", "cep": "24473", "tipo": "casa", "valor": 498926.13, "data_aquisicao": "2019-02-27"},
        ]
    }
    assert response.get_json() == expected_response
