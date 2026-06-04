# Analytics Service

## Descrição
Microsserviço agregador responsável por processar e formatar as métricas gerais do sistema para consumo do Dashboard Administrativo.

## Porta
5004

## Tecnologias
* Python
* Flask
* Requests

## Responsabilidades
* Consolidar dados do `user_service` e `loan_service`.
* Calcular multas em aberto, tempo médio de retorno e usuários ativos.
* Formatar dados mensais para os gráficos.

## Endpoints
* GET /analytics/dashboard

## Execução
pip install -r requirements.txt
python app.py