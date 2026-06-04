from pony.orm import *
import os

db = Database() #Criando o banco de dados

#Criando as tabela Livro

class Usuario(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    email = Required(str, unique=True)
    senha = Required(str)
    tipo = Required(str)  # "admin" ou "usuario"
    ativo = Required(bool, default=True)

#Conectando com o banco de dados 
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sqlite')
db.bind(provider='sqlite', filename=db_path, create_db=True)

#Mapeando/Criando tabela livro no banco de dados
db.generate_mapping(create_tables=True)