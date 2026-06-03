from pony.orm import *
from datetime import datetime, timezone

db = Database() #Criando o banco de dados

#Criando as tabela Livro



class Livro(db.Entity):
    id = PrimaryKey(int, auto=True)

    nome = Required(str, unique=True)
    autor = Required(str)
    categoria = Required(str)

    ano_publicacao = Required(int)

    disponivel = Required(bool, default=True)

    criado_em = Required(datetime,default=lambda: datetime.now(timezone.utc))



#Conectando com o banco de dados 
db.bind(provider='sqlite', filename='database.sqlite', create_db=False)

#Mapeando/Criando tabela livro no banco de dados
db.generate_mapping(create_tables=True)