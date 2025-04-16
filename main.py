from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, URL
from utils import generate_short_code   

Base.metadata.create_all(bind=engine)

app = FastAPI()

class URLRequest(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_unique_short_code(db: Session, length=6):
    while True:
        code = generate_short_code(length)
        if not db.query(URL).filter(URL.short_code == code).first():
            return code


@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_code = generate_unique_short_code(db)
    new_entry =URL(original_url=str(request.url), short_code=short_code)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"short_url":f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if url_entry:
        return RedirectResponse(url_entry.original_url)
    raise HTTPException(status_code=404, detail="URL not found")

