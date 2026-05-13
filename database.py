from sqlalchemy import create_engine, Column, Integer, String, Boolean, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./glp_rrhh.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la base de datos
class PostulanteDB(Base):
    __tablename__ = "postulantes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    dni = Column(String, unique=True, index=True)
    ex_fuerza_seguridad = Column(Boolean)
    estado = Column(String)
    tipo_rechazo = Column(String, nullable=True)
    motivo_rechazo = Column(String, nullable=True)
    
# crear las tablas
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()