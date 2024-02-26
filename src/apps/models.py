from sqlalchemy import Column, Integer, String

from settings.database import BaseDB, engine


class Character(BaseDB):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(Integer)
    
# BaseDB.metadata.create_all(bind=engine)