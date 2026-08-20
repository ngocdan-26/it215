from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL = "mysql+pymysql://root:021206@localhost:3306/btth_ss20"

engine = create_engine(URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()