# Payment Service

## Descrição
Microsserviço de simulação de pagamentos, responsável por registrar e processar as transações financeiras de multas de atraso.

## Porta
5005

## Tecnologias
* Python
* Flask
* Pony ORM
* SQLite

## Responsabilidades
* Simular verificação de dados de cartão de crédito.
* Salvar histórico de transações e recibos.

## Endpoints
* POST /payments/pay

## Execução
pip install -r requirements.txt
python app.py