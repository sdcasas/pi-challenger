from typing import Dict, Any

from starlette.exceptions import HTTPException


class BaseHttpException(HTTPException):
    status_code: int = None
    detail: str = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CharacterDoesNotExist(BaseHttpException):
    status_code = 404
    detail = 'Character not found'


class CharacterAlreadyExistsException(BaseHttpException):
    status_code = 400
    detail = 'Character already exists with the id'


class DataIntegrityErrorException(BaseHttpException):
    status_code = 409
    detail = 'Data integrity error'
