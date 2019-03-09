from enum import Enum


class Messages(Enum):
    STRANGE_ERROR: str = 'An error ocurred.'
    SUCCESS: str = 'Success.'
    TOKEN_INVALID: str = 'Token invalid.'
    ZIPCODE_INVALID: str = 'Zipcode invalid.'
    ZIPCODE_NOT_FOUND: str = 'Zip code not found.'
