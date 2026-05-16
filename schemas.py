from pydantic import BaseModel,  EmailStr
from typing import Annotated, Optional, List
from enum import Enum


class EstadoFase(str, Enum):
    ENTREVISTA = "ENTREVISTA"
    DOCUMENTACION = "DOCUMENTACION"
    RECHAZADO = "RECHAZADO"
    
class Entrevistado(BaseModel):
    nombre: str
    apellido: str
    dni: str
    ex_fuerza_seguridad: bool
    
class TipoRechazo(str, Enum):
    DEFINITIVO = "DEFINITIVO"
    TEMPORAL = "TEMPORAL"
    
class Postulante(Entrevistado):
    id: int
    estado: EstadoFase
    motivo_rechazo: Optional[str] = None