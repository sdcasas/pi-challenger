from pydantic import BaseModel


class Character(BaseModel):
    id: int
    name: str
    height: int
    mass: int
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: int
    
    class Config:
        orm_mode = True


class CharacterDelete(BaseModel):
    detail: str
    