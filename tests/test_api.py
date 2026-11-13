from fastapi.testclient import TestClient
from main import app
client=TestClient(app)
def test_health(): assert client.get("/health").status_code==200
def test_cpf():
    assert client.post("/validate/cpf",json={"value":"529.982.247-25"}).json()["valid"]
    assert not client.post("/validate/cpf",json={"value":"111.111.111-11"}).json()["valid"]
def test_cnpj():
    assert client.post("/validate/cnpj",json={"value":"11.222.333/0001-81"}).json()["valid"]
    assert not client.post("/validate/cnpj",json={"value":"11.222.333/0001-82"}).json()["valid"]
def test_phone(): assert client.post("/normalize/phone",json={"value":"(11) 99999-8888"}).json()["e164"]=="+5511999998888"
def test_csv(): assert client.post("/convert/csv-json",json={"csv_text":"name,age\nAna,20"}).json()["count"]==1
def test_demo(): assert "AgentData API" in client.get("/").text
def test_catalog(): assert client.get("/catalog").json()["payment_status"]=="demo_only"
