import os
from flask import Flask, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__)

USER_SERVICE = os.environ.get('USER_SERVICE_URL', 'http://localhost:5001')
LOAN_SERVICE = os.environ.get('LOAN_SERVICE_URL', 'http://localhost:5003')

@app.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        users_resp = requests.get(f'{USER_SERVICE}/users')
        users = users_resp.json() if users_resp.status_code == 200 else []
        
        loans_resp = requests.get(f'{LOAN_SERVICE}/loans')
        loans = loans_resp.json() if loans_resp.status_code == 200 else []
        
        total_alugueis = len(loans)
        usuarios_ativos = len([u for u in users if u.get('ativo', True) and u.get('tipo') != 'admin'])
        
        hoje = datetime.now(timezone.utc)
        
        emprestimos_atrasados = 0
        total_dias_retorno = 0
        qtd_devolvidos = 0
        
        alugueis_por_mes = {str(i): 0 for i in range(1, 13)}
        lucro_por_mes = {str(i): 0.0 for i in range(1, 13)}
        
        for loan in loans:
            if not loan.get('data_emprestimo'):
                continue
                
            dt_emp = datetime.fromisoformat(loan['data_emprestimo'].replace('Z', '+00:00'))
            mes_emp = str(dt_emp.month)
            alugueis_por_mes[mes_emp] += 1
            
            prazo = dt_emp.timestamp() + (14 * 86400)
            
            if loan['status'] in ['ativo', 'atrasado']:
                if hoje.timestamp() > prazo:
                    emprestimos_atrasados += 1
                    dias_atraso = int((hoje.timestamp() - prazo) / 86400)
                    lucro_por_mes[str(hoje.month)] += (dias_atraso * 2.5)
            elif loan['status'] == 'devolvido' and loan.get('data_devolucao'):
                dt_dev = datetime.fromisoformat(loan['data_devolucao'].replace('Z', '+00:00'))
                qtd_devolvidos += 1
                total_dias_retorno += (dt_dev.timestamp() - dt_emp.timestamp()) / 86400
                
                if dt_dev.timestamp() > prazo:
                    dias_atraso = int((dt_dev.timestamp() - prazo) / 86400)
                    lucro_por_mes[str(dt_dev.month)] += (dias_atraso * 2.5)
                    
        tempo_medio = (total_dias_retorno / qtd_devolvidos) if qtd_devolvidos > 0 else 0
        
        return jsonify({
            "total_alugueis": total_alugueis,
            "usuarios_ativos": usuarios_ativos,
            "emprestimos_atrasados": emprestimos_atrasados,
            "tempo_medio_retorno": round(tempo_medio, 1),
            "alugueis_por_mes": alugueis_por_mes,
            "lucro_por_mes": lucro_por_mes
        }), 200
    except Exception as e:
        return jsonify({"Status": "Erro ao gerar analytics", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)