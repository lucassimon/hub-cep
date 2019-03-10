from os import getenv
from abc import ABC, abstractmethod
from typing import Any
import requests
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    ContentDecodingError,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    Timeout,
    TooManyRedirects
)

from .exceptions import ZipcodeError, TokenError
from .messages import Messages


class AbstractProvider(ABC):

    API_URL = ''

    def __init__(self, zipcode):
        if zipcode is None or not zipcode:
            raise ZipcodeError(Messages.ZIPCODE_INVALID.value)

        self._zipcode = zipcode

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode: str):
        self._zipcode = zipcode

    def call(self, url: str, headers: dict = {}):
        error: bool = False
        info: dict = {}
        res: Any = None

        try:
            res = requests.get(url, headers=headers, timeout=int(getenv('TIMEOUT', default=3)))
            return False, {'error': error, 'timeout': False, 'message': Messages.SUCCESS.value}, res

        except ConnectionError as e:
            error = True
            info = {'error': error, 'timeout': False, 'message': e.args[0].reason.message}
            return error, info, res

        except (
            HTTPError, ProxyError, SSLError, Timeout,
            ConnectTimeout, ReadTimeout, TooManyRedirects, ContentDecodingError
        ) as e:
            error = True
            info = {'error': error, 'timeout': True, 'message': e.__str__()}
            return error, info, res

        except Exception as e:
            error = True
            info = {'error': error, 'timeout': False, 'message': e.__str__()}
            return error, info, res

        else:
            res.close()

        error = True
        info = {'error': error, 'timeout': False, 'message': Messages.STRANGE_ERROR.value}

        return error, info, res

    @abstractmethod
    def search():
        raise NotImplementedError(Messages.NOT_IMPLEMENTED.value)

    @abstractmethod
    def translate():
        raise NotImplementedError(Messages.NOT_IMPLEMENTED.value)


class Postmon(AbstractProvider):

    API_URL: str = 'http://api.postmon.com.br/v1/cep/'

    def get_url(self):
        return f'{self.API_URL}{self.zipcode}'

    def search(self):
        '''
        This is a method to get address info from an API
        '''
        error = True
        info = {'error': error, 'timeout': False, 'message': Messages.STRANGE_ERROR.value}

        url = self.get_url()

        error, info, res = self.call(url)

        if error:
            return error, info

        if res.status_code == requests.codes.ok:
            data = self.translate(res.json())
            info = {'error': error, 'message': Messages.SUCCESS.value, 'data': data}
            return error, info

        elif (
            res.status_code == requests.codes.not_found
            or res.status_code == requests.codes.not_allowed
        ):
            error = True
            info = {'error': error, 'message': Messages.ZIPCODE_NOT_FOUND.value}
            return error, info

        else:
            error = True
            info = {'error': error, 'message': Messages.STRANGE_ERROR.value}
            return error, info

    def translate(self, info: dict):

        return {
            'zip_code': info.get('cep'),
            'address': info.get('logradouro'),
            'number': '',
            'info': '',
            'district': info.get('bairro'),
            'city': info.get('cidade'),
            'state': info.get('estado'),
            'country': 'BRA'
        }


class Viacep(AbstractProvider):

    API_URL: str = 'http://viacep.com.br/ws/{}/json/unicode/'

    def get_url(self):
        return self.API_URL.format(self.zipcode)

    def search(self):
        error = True
        info = {'error': error, 'message': Messages.STRANGE_ERROR.value}

        url = self.get_url()

        error, info, res = self.call(url)

        if error:
            return error, info

        if res.status_code == requests.codes.ok:
            data = self.translate(res.json())
            info = {'error': error, 'message': Messages.SUCCESS.value, 'data': data}
            return error, info

        elif (
            res.status_code == requests.codes.not_found
            or res.status_code == requests.codes.bad
        ):
            error = True
            info = {'error': error, 'message': Messages.ZIPCODE_NOT_FOUND.value}
            return error, info

        else:
            error = True
            info = {'error': error, 'message': Messages.STRANGE_ERROR.value}
            return error, info

    def translate(self, info: dict):

        return {
            'zip_code': info.get('cep'),
            'address': info.get('logradouro'),
            'number': '',
            'info': '',
            'district': info.get('bairro'),
            'city': info.get('localidade'),
            'state': info.get('uf'),
            'country': 'BRA'
        }


class Cepaberto(AbstractProvider):

    API_URL = 'http://www.cepaberto.com/api/v3/cep?cep={}'

    def __init__(self, zipcode: str, token: str):
        super().__init__(zipcode)
        # Is valid zip_code param
        if token is None or not token:
            raise TokenError(Messages.TOKEN_INVALID.value)

        self._token = token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    def get_url(self):
        return self.API_URL.format(self.zipcode)

    def get_headers(self):
        return {'Authorization': f'Token token={self.token}'}

    def search(self):
        error = True
        info = {'error': error, 'message': Messages.STRANGE_ERROR.value}

        url = self.get_url()

        error, info, res = self.call(url, self.get_headers())

        if error:
            return error, info

        if res.status_code == requests.codes.ok:
            data = self.translate(res.json())
            info = {'error': error, 'message': Messages.SUCCESS.value, 'data': data}
            return error, info

        elif (
            res.status_code == requests.codes.not_found
            or res.status_code == requests.codes.server_error
        ):
            error = True
            info = {'error': error, 'message': Messages.ZIPCODE_NOT_FOUND.value}
            return error, info

        else:
            error = True
            info = {'error': error, 'message': Messages.STRANGE_ERROR.value}
            return error, info

    def translate(self, info: dict):

        return {
            'zip_code': info.get('cep'),
            'address': info.get('logradouro'),
            'number': '',
            'info': '',
            'district': info.get('bairro'),
            'city': info.get('cidade', '').get('nome', ''),
            'state': info.get('estado', '').get('sigla', ''),
            'country': 'BRA'
        }
