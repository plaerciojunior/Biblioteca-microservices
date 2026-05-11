from pony.orm import *
from datetime import datetime, timezone

db = Database()

class Emprestimo(db.Entity):

    id = PrimaryKey(int, auto=True)

    usuario_id = Required(int)

    livro_id = Required(int)

    data_emprestimo = Required(
        datetime,
        default=lambda: datetime.now(timezone.utc)
    )

    data_devolucao = Optional(datetime)

    status = Required(str, default='ativo')


db.bind(provider='sqlite', filename='database.sqlite', create_db=False)

db.generate_mapping(create_tables=True)