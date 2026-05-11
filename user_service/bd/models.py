from pony.orm import *

db = Database() #Criando o banco de dados

#Criando as tabela Livro

class Usuario(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    email = Required(str, unique=True)
    senha = Required(str)
    tipo = Required(str)  # "admin" ou "usuario"

#Conectando com o banco de dados 
db.bind(provider='sqlite', filename='database.sqlite', create_db=False)

#Mapeando/Criando tabela livro no banco de dados
db.generate_mapping(create_tables=True)