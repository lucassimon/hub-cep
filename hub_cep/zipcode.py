
from os import getenv
from abc import ABC, abstractmethod

from .exceptions import ZipcodeError
from .messages import Messages
from .providers import Viacep, Postmon, Cepaberto


class AbstractZipCode(ABC):

    def __init__(self, zipcode: str):
        if zipcode is None or not zipcode:
            raise ZipcodeError(Messages.ZIPCODE_INVALID.value)

        self._zipcode = zipcode

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode: str):
        self._zipcode = zipcode

    @abstractmethod
    def search():
        raise NotImplementedError(Messages.NOT_IMPLEMENTED.value)


class ZipCode(AbstractZipCode):

    def __init__(self, zipcode: str):
        super().__init__(zipcode)

        self.viacep = Viacep(zipcode)
        self.postmon = Postmon(zipcode)
        self.cepaberto = None

        token = getenv('CEPABERTO_TOKEN', default='')

        if token:
            self.cepaberto = Cepaberto(zipcode, token)

    def search(self):

        error, data = self.viacep.search()

        if not error:
            return 200, data

        error, data = self.postmon.search()

        if not error:
            return 200, data

        if self.cepaberto:
            error, data = self.cepaberto.search()

            if not error:
                return 200, data

        return 422, data
