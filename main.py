from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db, PostulanteDB, SessionLocal
from schemas import Entrevistado, Postulante, TipoRechazo, EstadoFase

app = FastAPI(title="Sistema RR.HH - GLP")

# Fase 1: Entrevista
# Definimos los estados posibles para la fase de entrevista


# Registramos persona entrevistada y si fue aceptada o rechazada
#Si es aceptada cargamos datos basicos y pasamos a la fase de documentación
#Si es rechazada cargamos motivo de rechazo y pasamos a fase de rechazo definiendo si es definitvo o puede volver a postular en el futuro
@app.post("/postulantes/entrevista", response_model=Postulante)
def registrar_entrevista(
    entrevistado: Entrevistado,
    aceptado: bool,
    tipo_rechazo: Optional[TipoRechazo] = None,
    motivo_rechazo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Determinamos el estado
    nuevo_estado = EstadoFase.DOCUMENTACION if aceptado else EstadoFase.RECHAZADO
    
    # Determinamos BD
    db_postulante = PostulanteDB(
        nombre = entrevistado.nombre,
        apellido = entrevistado.apellido,
        dni = entrevistado.dni,
        ex_fuerza_seguridad = entrevistado.ex_fuerza_seguridad,
        estado = nuevo_estado,
        tipo_rechazo = tipo_rechazo.value if tipo_rechazo else None,
        motivo_rechazo = motivo_rechazo if not aceptado else None
    )
    
    try:
        db.add(db_postulante)
        db.commit()
        db.refresh(db_postulante)
        
        return db_postulante
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar entrevista: {str(e)}")
    
@app.get("/postulantes", response_model=List[Postulante])
def obtener_postulantes(db: Session = Depends(get_db)):
    postulantes = db.query(PostulanteDB).all()
    return postulantes
    



