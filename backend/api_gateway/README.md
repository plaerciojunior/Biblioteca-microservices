# API Gateway

## Descrição

O API Gateway é responsável por centralizar as requisições do sistema e encaminhá-las para os microsserviços apropriados.

Todos os clientes (frontend) devem se comunicar apenas com o Gateway.

## Porta

5000

## Tecnologias

* Python
* Flask
* Flask-CORS
* Requests

## Microsserviços Integrados

* User Service (5001)
* Book Service (5002)
* Loan Service (5003)

## Responsabilidades

* Receber requisições do frontend
* Encaminhar requisições para os microsserviços
* Retornar respostas unificadas ao cliente
* Configurar CORS para permitir integração com aplicações frontend

## Execução

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

Consulte a documentação completa em:

`../docs/API.md`
