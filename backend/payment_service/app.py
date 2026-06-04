from flask import Flask, jsonify, request
from pony.orm import db_session, commit
from bd.models import db, Pagamento
import os

app = Flask(__name__)

@app.route('/payments/pay', methods=['POST'])
@db_session
def processar_pagamento():
    data = request.json
    usuario_id = data.get('usuario_id')
    valor = data.get('valor')
    cartao = data.get('cartao', '0000')

    if not usuario_id or not valor:
        return jsonify({"Status": "Dados inválidos"}), 400

    # Mock de processamento seguro (salva apenas os últimos 4 dígitos)
    cartao_mascarado = f"**** **** **** {cartao[-4:]}" if len(cartao) >= 4 else "****"

    Pagamento(
        usuario_id=usuario_id,
        valor=float(valor),
        cartao_mascarado=cartao_mascarado
    )
    commit()
    return jsonify({"Status": "Pagamento processado com sucesso!"}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)