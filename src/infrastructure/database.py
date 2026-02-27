from pathlib import Path

from sqlmodel import Session, create_engine

from src.domain.models import Vehicle

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "vehicles.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
