from sqlalchemy import Column, String # Importa os tipos de coluna e tipos básicos do SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID # Importa o tipo UUID específico do PostgreSQL
import uuid 

from .database import Base


class User(Base):
    __tablename__ = "users"  # nome real da tabela no PostgreSQL

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False, unique=True) #modifiquei do enunciado
    role = Column(String, nullable=True)
