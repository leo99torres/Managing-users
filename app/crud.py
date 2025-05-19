from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from typing import Optional

#Função para buscar todos os usuários no banco
def get_users(db: Session):
    return db.query(models.User).order_by(models.User.name.asc()).all()

#Função para buscar um único usuário por ID
def get_user(db: Session, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first() #esse .first() evita excessões se o usuário não existir

#Função para buscar um único usuário por email
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


#Função para criar um novo usuário
def create_user(db: Session, user: schemas.UserCreate): # Cria um objeto User com os dados já validados do Pydantic
    
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role if user.role else None
    ) 

    db.add(db_user) # Adiciona o objeto à sessão do banco

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback() #da rollback se tiver pegado algum erro de unicidade

        # Comunica os erros, relativos ao banco de dados
        if "email" in str(e.orig):
            raise HTTPException(status_code=409, detail="Já existe um usuário com esse e-mail.")
        elif "phone" in str(e.orig):
            raise HTTPException(status_code=409, detail="Já existe um usuário com esse número de telefone.")
        else:
            raise HTTPException(status_code=409, detail="Violação de unicidade no banco de dados.")


    return db_user

#Função para atualizar um usuário existente
def update_user(db: Session, user_email, user_data: schemas.UserUpdate):
    user = get_user_by_email(db, user_email) # Cria um objeto User com os dados já validados do Pydantic

    if user:
        if user_data.name is not None:
            user.name = user_data.name

        if user_data.phone is not None and user_data.phone != user.phone:
            existing_user = db.query(models.User).filter(models.User.phone == user_data.phone).first()
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=409, detail="Já existe um usuário com esse número de telefone.")
            user.phone = user_data.phone

        if user_data.role is not None:
            user.role = user_data.role

        try:
            db.commit()
            db.refresh(user)
        
        except IntegrityError as e:
            db.rollback()

            if "email" in str(e.orig):
                raise HTTPException(status_code=409, detail="Já existe um usuário com esse e-mail.")
            elif "phone" in str(e.orig):
                raise HTTPException(status_code=409, detail="Já existe um usuário com esse número de telefone.")
            else:
                raise HTTPException(status_code=409, detail="Erro de integridade no banco.")
    
    return user

#Função para deletar um usuário
def delete_user(db: Session, email):
    user = get_user_by_email(db, email)  # Busca o usuário

    if user:
        db.delete(user)     # Marca o objeto para exclusão
        db.commit()         # Aplica a exclusão no banco

    return user  # Retorna o usuário deletado (ou None se não existir)
