# AgentData API — Demonstração gratuita

API FastAPI para validar dígitos verificadores de CPF/CNPJ, padronizar telefones brasileiros e converter CSV para JSON. **Não consulta cadastros, não comprova identidade e não recebe pagamentos.** Use somente dados fictícios nos testes.

## Testar localmente
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Abra http://127.0.0.1:8000 para a demonstração ou /docs para OpenAPI.

## Publicar na Render
1. Entre em https://dashboard.render.com/ e conecte sua conta GitHub.
2. Clique em **New > Blueprint** e selecione este repositório.
3. Revise o plano gratuito e confirme a criação. A Render gerará o endereço público.
4. Acesse o endereço gerado e teste /health, /docs e a página inicial.

O arquivo `render.yaml` configura Docker, o plano gratuito e a verificação de saúde. Serviços gratuitos podem hibernar e ter limitações de disponibilidade. **Não habilite pagamentos reais sem implementar autenticação, limites de requisição, proteção de dados e integração de pagamento validada.**

## Rotas
- `POST /validate/cpf` — `{"value":"529.982.247-25"}`
- `POST /validate/cnpj` — `{"value":"11.222.333/0001-81"}`
- `POST /normalize/phone` — `{"value":"(11) 99999-8888"}`
- `POST /convert/csv-json` — `{"csv_text":"name,age\nAna,20"}`
- `GET /health`, `GET /catalog`, `GET /openapi.json`

## Testes
```bash
pytest -q
```
O GitHub Actions também executa testes em cada envio.
