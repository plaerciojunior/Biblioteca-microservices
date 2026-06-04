# API Gateway

## Descrição

O API Gateway atua como a porta de entrada unificada para todas as requisições do frontend. Ele é responsável por rotear o tráfego para o microsserviço correto, garantindo que a complexidade da arquitetura interna do backend seja abstraída do cliente.

Todos os clientes (frontend) devem se comunicar apenas com o Gateway.

## Porta

5000

## Tecnologias

* Python
* Flask
* Flask-CORS
* Requests

## Microsserviços Integrados

* `user_service` (Porta 5001)
* `book_service` (Porta 5002)
* `loan_service` (Porta 5003)
* `analytics_service` (Porta 5004)
* `payment_service` (Porta 5005)

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
