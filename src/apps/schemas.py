from pydantic import BaseModel


class CharacterBasic(BaseModel):
    id: int
    name: str
    height: int
    mass: int
    eye_color: str
    birth_year: int


class Character(CharacterBasic):
    hair_color: str
    skin_color: str
    
    class Config:
        orm_mode = True


class CharacterDelete(BaseModel):
    detail: str
    