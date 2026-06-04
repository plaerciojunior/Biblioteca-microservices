from pony.orm import *
from datetime import datetime, timezone
import os

db = Database() #Criando o banco de dados

#Criando as tabela Livro



class Livro(db.Entity):
    id = PrimaryKey(int, auto=True)

    nome = Required(str, unique=True)
    autor = Required(str)
    categoria = Required(str)

    ano_publicacao = Required(int)

    pdf_url = Optional(str)

    disponivel = Required(bool, default=True)

    criado_em = Required(datetime,default=lambda: datetime.now(timezone.utc))



#Conectando com o banco de dados 
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sqlite')
db.bind(provider='sqlite', filename=db_path, create_db=True)

#Mapeando/Criando tabela livro no banco de dados
db.generate_mapping(create_tables=True)