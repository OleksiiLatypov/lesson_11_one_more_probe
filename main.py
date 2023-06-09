from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.param_functions import Path
from fastapi.params import Query
from sqlalchemy.orm import Session, query
from sqlalchemy import text
from pydantic import BaseModel, EmailStr, Field
from starlette import status

from connect_db import get_db
from models import Owner, Cat

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


class OwnerModel(BaseModel):
    email: EmailStr


class ResponseOwner(BaseModel):
    id: int = 1
    email: EmailStr

    class Config:
        orm_mode = True


@app.get('/owners', response_model=List[ResponseOwner], tags=['owners'])
async def get_owners(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners


@app.get('/owners/{owner_id}', response_model=ResponseOwner, tags=['owners'])
async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found')
    return owner


@app.post('/owners', response_model=ResponseOwner, tags=['owners'])
async def create_owners(body: OwnerModel, db: Session = Depends(get_db)):
    owner = Owner(**body.dict())  # email=body.email .... body is an instance of OwnerModel
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@app.put('/owners/{owner_id}', response_model=ResponseOwner, tags=['owners'])
async def update_owner(body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found')
    owner.email = body.email
    db.commit()
    return owner


@app.delete('/owners/{owner_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['owners'])
async def delete_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found')
    db.delete(owner)
    db.commit()
    # return owner


class PetModel(BaseModel):
    nickname: str = Field('Barsik', min_length=3, max_length=12)
    age: int = Field(1, ge=1, le=30)
    description: str
    vaccinated: bool = Field(False)
    owner_id: int = Field(gt=1)


class ResponsePet(BaseModel):
    id: int = 1
    nickname: str
    age: int
    vaccinated: bool
    description: str
    owner: ResponseOwner

    class Config:
        orm_mode = True


@app.get('/cats', response_model=List[PetModel], tags=['cats'])
async def get_cats(limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    cats = db.query(Cat).limit(limit).offset(offset).all()
    return cats


@app.get('/cats/{cat_id}', response_model=List[PetModel], tags=['cats'])
async def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found')
    return cat


@app.post('/cats', response_model=ResponsePet, tags=['cats'])
async def create_cat(body: PetModel, db: Session = Depends(get_db)):
    cat = PetModel(**body.dict())  # email=body.email .... body is an instance of OwnerModel
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat
