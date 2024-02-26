from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from apps.exceptions import CharacterDoesNotExist
from settings.database import get_db

from apps.services import CharacterCrud
from apps.schemas import Character as CharacterSchema, CharacterDelete


router = APIRouter()


@router.get("/getAll", status_code=status.HTTP_200_OK)
def get_all_characters(db: Session = Depends(get_db)) -> list[CharacterSchema]:
    return CharacterCrud(db).get_all()


@router.get("/get/{id}", status_code=status.HTTP_200_OK)
def get_character(response: Response, id: int, db: Session = Depends(get_db)) -> CharacterSchema:
    _character = CharacterCrud(db).get(id)
    if _character is None:
        raise CharacterDoesNotExist()
    return _character


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_character(character: CharacterSchema, db: Session = Depends(get_db)) -> CharacterSchema:
    new_character = CharacterCrud(db).create(data=character)
    return new_character


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
def delete_character(id: int, db: Session = Depends(get_db)) -> CharacterDelete:
    _action_delete = CharacterCrud(db).delete(id=id)
    return CharacterDelete(detail=f"Character with ID {id} deleted successfully")
