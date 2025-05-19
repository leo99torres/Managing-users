from fastapi import FastAPI, HTTPException #FastAPI: cria o app e define as rotas.
from fastapi import Depends #Cria dependência de conexão com o banco de dados
from sqlalchemy.orm import Session #Representa a conexão ativa com o banco de dados
from typing import List #Permite escrever que uma rota retorna uma lista de usuários
from fastapi.middleware.cors import CORSMiddleware


from . import models, schemas, crud
from .database import SessionLocal, engine

# Cria as tabelas no banco se ainda não existirem
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Adiciona o middleware de CORS para permitir que o frontend (ou outros clientes)
# façam requisições HTTP para esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True, #Não é o ideal em prod. 
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependência que abre e fecha uma sessão do banco
def get_db():
    db = SessionLocal() # Abre a conexão
    try:
        yield db
    finally:
        db.close()

#Listar todos os usuários
@app.get("/users", response_model=List[schemas.UserOut], tags=["Listar todos os usuários"])
def listar_usuarios(db: Session = Depends(get_db)):
    """Listar todos os usuários cadastrados."""
    return crud.get_users(db)

#Buscar um usuário por ID
@app.get("/users/{id}", response_model=schemas.UserOut, tags=["Busca de usuários"])
def buscar_usuario(id: str, db: Session = Depends(get_db)):
    """Buscar usuários pelo ID do banco."""
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

#Criar um novo usuário
@app.post("/users", response_model=schemas.UserOut, status_code=201, tags=["Cadastrar novos usuários"]) #O status HTTP 201 significa "Created"
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Cadastrar novos usuários."""
    return crud.create_user(db, user)

#atualizar um usuário pelo email
@app.put("/users/by-email/{email}", response_model=schemas.UserOut, tags=["Editar dados de usuários"])
def atualizar_usuario_por_email(email: str, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Atualizar dados dos usuários a partir do email."""
    user = crud.update_user(db, email, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


#Deletar um usuário
@app.delete("/users/by-email/{email}", response_model=schemas.UserOut, tags=["Deletar usuários"])
def deletar_usuario_por_email(email: str, db: Session = Depends(get_db)):
    """Deletar usuários por email."""
    user = crud.delete_user(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

#rota de busca por email
@app.get("/users/by-email/{email}", response_model=schemas.UserOut, tags=["Busca de usuários"])
def buscar_email(email : str, db: Session = Depends(get_db)):
    """Buscar usuários por email."""
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

