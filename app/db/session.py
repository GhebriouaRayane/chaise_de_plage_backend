from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

db_url = make_url(settings.DATABASE_URL)
engine_kwargs = {"pool_pre_ping": True}

if db_url.get_backend_name().startswith("postgresql"):
    query = dict(db_url.query)
    query.pop("pgbouncer", None)
    if "sslmode" not in query:
        query["sslmode"] = "require"
    db_url = db_url.set(query=query)

# SQLite is handy for local development because it does not require Postgres.
if db_url.get_backend_name() == "sqlite":
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(db_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
