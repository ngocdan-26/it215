from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/learning_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    document_type = Column(String(100), nullable=False)
    file_url = Column(String(500), nullable=False)

Base.metadata.create_all(bind=engine)

class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(DocumentModel).all()
    return {
        "message": "Lấy danh sách tài liệu thành công",
        "data": documents
    }

@app.post("/documents")
def create_document(document: DocumentCreate,db: Session = Depends(get_db)):
    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Thêm tài liệu thành công",
        "data": {
            "id": new_document.id,
            "title": new_document.title,
            "subject": new_document.subject,
            "document_type": new_document.document_type,
            "file_url": new_document.file_url
        }
    }

@app.delete("/documents/{document_id}")
def delete_document(document_id: int,db: Session = Depends(get_db)):
    document = (db.query(DocumentModel).filter(DocumentModel.id == document_id).first())
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    db.delete(document)
    db.commit()
    return {
        "message": "Xóa tài liệu thành công"
    }