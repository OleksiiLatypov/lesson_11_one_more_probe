from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, query
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from connect_db import get_db
from models import Owner

app = FastAPI()


@app.get('/', name='Alex')
def read_root():
    return {'message': 'ReatAPP v1.0'}


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {'message': 'Welcome to FastAPI !'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error connecting to database')


@app.get('/owners')
async def get_owners(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners


class OwnerModel(BaseModel):
    email: EmailStr


@app.post('/owners')
async def create_owners(body: OwnerModel, db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners
