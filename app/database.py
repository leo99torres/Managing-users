from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://leandrotorres@localhost/meu_crud"

engine = create_engine(SQLALCHEMY_DATABASE_URL) #Cria e gera sessões no banco de dados
#engine é usado pelo ORM para executar comandos SQL.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #Cria um mapeamento entre a tabela SQL e a classe Python, 
#Classe que vai “registrar” os modelos como tabelas

