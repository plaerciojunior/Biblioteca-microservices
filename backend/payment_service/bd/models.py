from pony.orm import *
from datetime import datetime, timezone
import os

db = Database()

class Pagamento(db.Entity):
    id = PrimaryKey(int, auto=True)
    usuario_id = Required(int)
    valor = Required(float)
    cartao_mascarado = Required(str)
    data_pagamento = Required(datetime, default=lambda: datetime.now(timezone.utc))
    status = Required(str, default="sucesso")

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sqlite')
db.bind(provider='sqlite', filename=db_path, create_db=True)

db.generate_mapping(create_tables=True)