from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Note
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/notes',
    tags= ['notes']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class NoteRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=250)


'''@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Note).filter(Note.user_id == user.get('user_id')).all()'''

@router.get("/notes/", status_code=status.HTTP_200_OK)
async def get_user_notes(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    notes = db.query(Note).filter(Note.user_id == user.get("user_id")).all()
    if not notes:
        return []
    return notes

@router.get("/note/{note_id}/", status_code=status.HTTP_200_OK)
async def read_note(user: user_dependency, db: db_dependency, note_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
#    note_model = db.query(Note).filter(Note.note_id == note_id).filter(Note.user_id == user.get('user_id')).first()
#    note_model = db.query(Note).filter(Note.note_id == note_id, Note.user_id == user.get('user_id')).first()
    note_model = db.query(Note).filter(Note.user_id == user.get('user_id')).all()
    if note_model is not None:
        return note_model
    raise HTTPException(status_code=404, detail='Note not found.')


@router.post("/note/", status_code=status.HTTP_201_CREATED)
async def create_note(user: user_dependency, db: db_dependency,
                      note_request: NoteRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    note_model = Note(**note_request.model_dump(), user_id=user.get('user_id'))

    db.add(note_model)
    db.commit()


@router.put("/note/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(user: user_dependency, db: db_dependency,
                      note_request: NoteRequest,
                      note_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    note_model = db.query(Note).filter(Note.note_id == note_id)\
        .filter(Note.user_id == user.get('user_id')).first()
    if note_model is None:
        raise HTTPException(status_code=404, detail='Note not found.')

    note_model.title = note_request.title
    note_model.description = note_request.description

    db.add(note_model)
    db.commit()


@router.delete("/note/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(user: user_dependency, db: db_dependency, note_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    note_model = db.query(Note).filter(Note.note_id == note_id)\
        .filter(Note.user_id == user.get('user_id')).first()
    if note_model is None:
        raise HTTPException(status_code=404, detail='Note not found.')
    db.query(Note).filter(Note.note_id == note_id).filter(Note.user_id == user.get('user_id')).delete()

    db.commit()
