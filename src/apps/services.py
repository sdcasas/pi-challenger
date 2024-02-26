import logging

from sqlalchemy.orm import Session

from apps.exceptions import DataIntegrityErrorException, CharacterAlreadyExistsException, CharacterDoesNotExist
from apps.models import Character
from apps.schemas import Character as CharacterSchema


class CharacterCrud:
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Character).all()

    def get(self, id: int):
        try:
            return self.db.query(Character).filter(Character.id==id).first()
        except Exception as e:
            logging.info(f"Error get Character, id {str(id)}, msg: {str(e)}")
            return None

    def create(self, data: CharacterSchema):
        if self.get(id=data.id):
            raise CharacterAlreadyExistsException()
        try:
            db_character = Character(**data.dict())
            self.db.add(db_character)
            self.db.commit()
            self.db.refresh(db_character)
        except Exception as e:
            self.db.rollback()
            logging.critical(msg=f'Error in create Character {data.__dict__} Error: {str(e)}')
            raise DataIntegrityErrorException()
        return db_character

    def delete(self, id: int):
        character = self.get(id=id)
        if character is None:
            raise CharacterDoesNotExist()
        self.db.delete(character)
        self.db.commit()