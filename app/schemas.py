from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID
import re

PhoneStr = str  # Tipo simples, sem validação automática

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None


class UserCreate(UserBase):
    phone: PhoneStr

    @field_validator('phone') #sintaxe moderna do Pydantic v2
    @classmethod
    def validate_phone_message(cls, v):
        # Remove espaços, traços e sinal de +
        v = v.replace(" ", "").replace("-", "").replace("+", "").replace("(", "").replace(")","")

        if len(v) > 9:
        # Remove zero à esquerda se for prefixo antes do DDD
            if v.startswith("0"):
                v = v[1:]
            # Adiciona DDI "55" se ainda não tiver
            if not v.startswith("55"):
                v = "55" + v


        if not re.fullmatch(r'\d{9,19}', v):
            raise ValueError("Telefone inválido: use apenas dígitos, entre 9 e 15 caracteres.")
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
    role: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone_message(cls, v):
        # Remove espaços, traços e sinal de + e ()
        v = v.replace(" ", "").replace("-", "").replace("+", "").replace("(", "").replace(")","")
        # Se tiver mais que 9 dígitos, assume que tem DDD
        
        if len(v) > 9:
            # Remove zero à esquerda se for prefixo antes do DDD
            if v.startswith("0"):
                v = v[1:]
            # Adiciona DDI "55" se ainda não tiver
            if not v.startswith("55"):
                v = "55" + v

        if v is not None and not re.fullmatch(r'\d{9,19}', v):
            raise ValueError("Telefone inválido: use apenas dígitos, entre 9 e 15 caracteres.")
        return v

class UserOut(UserBase):
    id: UUID
    phone: PhoneStr

    model_config = {
        "from_attributes": True
    }
