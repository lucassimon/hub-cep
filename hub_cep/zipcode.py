from os import getenv
from abc import ABC, abstractmethod

from .exceptions import TokenError

from .providers import Viacep, Postmon, Cepaberto


class AbstractZipCode(ABC):

    def __init__(self, zipcode: str):
        self._zipcode = zipcode

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode: str):
        self._zipcode = zipcode

    @abstractmethod
    def search(self):
        pass


class ZipCode(AbstractZipCode):

    def __init__(self, zipcode: str):
        super().__init__(zipcode)

        self.viacep = Viacep(zipcode)
        self.postmon = Postmon(zipcode)

        try:
            token = getenv('CEPABERTO_TOKEN', default='')
            self.cepaberto = Cepaberto(zipcode, token)

        except TokenError:
            self.cepaberto = None

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
