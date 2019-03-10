from os import getenv
import pytest
from dotenv import load_dotenv
from requests import Session
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

from hub_cep.providers import AbstractProvider, Postmon, Viacep, Cepaberto
from hub_cep.exceptions import ZipcodeError, TokenError


ZIPCODE = '78048000'
INVALID_ZIPCODE = '3111111'

load_dotenv()


class TestAbstractProvider:

    @pytest.fixture(scope='class')
    def data(self):
        obj = AbstractProvider
        return obj

    def test_raises_not_implemented_error_when_call_search_method(self, data):
        with pytest.raises(NotImplementedError) as e:
            data.search()

        assert e.value.args[0] == 'Should implement.'

    def test_raises_not_implemented_error_when_call_translate_method(self, data):
        with pytest.raises(NotImplementedError) as e:
            data.translate()

        assert e.value.args[0] == 'Should implement.'


class TestViacep:

    FAKE_BASE_URL = 'http://viacep.com.br/ws/{}/json/unicode/'
    FAKE_URL = FAKE_BASE_URL.format(ZIPCODE)

    @pytest.fixture()
    def viacep_success(self, requests_mock):

        fake_response = {
            'cep': '78048-000',
            'logradouro': 'Avenida Miguel Sutil',
            'bairro': 'Alvorada',
            'localidade': 'Cuiabá',
            'uf': 'MT',
        }

        requests_mock.get(TestViacep.FAKE_URL, json=fake_response, status_code=200)
        client = Viacep(ZIPCODE)
        error, result = client.search()
        return result

    def test_base_url(self):
        assert Viacep.API_URL == TestViacep.FAKE_BASE_URL

    def test_get_url(self):
        client = Viacep(ZIPCODE)
        assert client.get_url() == TestViacep.FAKE_URL

    def test_zipcode_getter(self):
        client = Viacep(ZIPCODE)
        assert client.zipcode == ZIPCODE

    def test_zipcode_setter(self):
        client = Viacep(ZIPCODE)
        client.zipcode = INVALID_ZIPCODE
        assert client.zipcode == INVALID_ZIPCODE

    def test_estado(self, viacep_success):
        assert viacep_success.get('data').get('state') == 'MT'

    def test_localidade(self, viacep_success):
        assert viacep_success.get('data').get('city') == 'Cuiabá'

    def test_bairro(self, viacep_success):
        assert viacep_success.get('data').get('district') == 'Alvorada'

    def test_endereco(self, viacep_success):
        assert viacep_success.get('data').get('address') == 'Avenida Miguel Sutil'

    def test_data_invalid(self):
        client = Viacep(INVALID_ZIPCODE)
        error, data = client.search()
        assert error is True

    def test_raises_zipcode_error(self):
        with pytest.raises(ZipcodeError) as e:
            Viacep('')

        assert e.value.args[0] == 'Zipcode invalid.'

    def test_raises_connection_timeout_on_request(self, requests_mock):
        client = Viacep(ZIPCODE)
        requests_mock._adapter.register_uri('GET', TestViacep.FAKE_URL, exc=ConnectTimeout('Timeout'))
        error, info, res = client.call(TestViacep.FAKE_URL)

        assert error is True
        assert info == {'error': True, 'timeout': True, 'message': 'Timeout'}
        assert res is None

    def test_raises_http_error_on_request(self, requests_mock):
        client = Viacep(ZIPCODE)
        requests_mock._adapter.register_uri('GET', TestViacep.FAKE_URL, exc=HTTPError('Http Error'))
        error, info, res = client.call(TestViacep.FAKE_URL)

        assert error is True
        assert info == {'error': True, 'timeout': True, 'message': 'Http Error'}
        assert res is None

    def test_raises_connection_error_on_request(self, requests_mock):
        client = Viacep(ZIPCODE)
        requests_mock._adapter.register_uri('GET', TestViacep.FAKE_URL, exc=ConnectionError)
        error, info, res = client.call(TestViacep.FAKE_URL)

        assert error is True
        assert info == {'error': True, 'timeout': False, 'message': 'Network error.'}
        assert res is None

    def test_raises_exception_on_request(self, requests_mock):
        client = Viacep(ZIPCODE)
        requests_mock._adapter.register_uri('GET', TestViacep.FAKE_URL, exc=Exception('Some error'))
        error, info, res = client.call(TestViacep.FAKE_URL)

        assert error is True
        assert info == {'error': True, 'timeout': False, 'message': 'Some error'}
        assert res is None

    def test_returns_error_info_when_search_with_raises_any_exception(self, requests_mock):
        client = Viacep(ZIPCODE)
        requests_mock._adapter.register_uri('GET', TestViacep.FAKE_URL, exc=Exception('Some error'))
        error, info, = client.search()

        assert error is True
        assert info == {'error': True, 'timeout': False, 'message': 'Some error'}

    def test_returns_error_info_when_requests_responses_any_status_codes(self, requests_mock):
        requests_mock.get(TestViacep.FAKE_URL, status_code=406)
        client = Viacep(ZIPCODE)
        error, result = client.search()
        assert result == {'error': True, 'message': 'An error ocurred.'}


class TestPostmon:

    FAKE_BASE_URL = 'http://api.postmon.com.br/v1/cep/'
    FAKE_URL = f'{FAKE_BASE_URL}{ZIPCODE}'

    @pytest.fixture()
    def postmon_success(self, requests_mock):

        fake_response = {
            'cep': '78048-000',
            'logradouro': 'Avenida Miguel Sutil',
            'bairro': 'Alvorada',
            'cidade': 'Cuiabá',
            'estado': 'MT',
        }

        requests_mock.get(TestPostmon.FAKE_URL, json=fake_response, status_code=200)
        client = Postmon(ZIPCODE)
        error, result = client.search()
        return result

    def test_base_url(self):
        assert Postmon.API_URL == TestPostmon.FAKE_BASE_URL

    def test_get_url(self):
        client = Postmon(ZIPCODE)
        assert client.get_url() == TestPostmon.FAKE_URL

    def test_estado(self, postmon_success):
        assert postmon_success.get('data').get('state') == 'MT'

    def test_localidade(self, postmon_success):
        assert postmon_success.get('data').get('city') == 'Cuiabá'

    def test_bairro(self, postmon_success):
        assert postmon_success.get('data').get('district') == 'Alvorada'

    def test_endereco(self, postmon_success):
        assert postmon_success.get('data').get('address') == 'Avenida Miguel Sutil'

    def test_invalid_zipcode(self):
        client = Postmon(INVALID_ZIPCODE)
        error, data = client.search()
        assert error is True


class TestCepaberto:

    FAKE_BASE_URL = 'http://www.cepaberto.com/api/v3/cep?cep={}'
    FAKE_URL = FAKE_BASE_URL.format(ZIPCODE)

    @pytest.fixture()
    def cepaberto_success(self, requests_mock):

        fake_response = {
            'cep': '78048-000',
            'logradouro': 'Avenida Miguel Sutil, de 5799/5800 a 7887/7888',
            'bairro': 'Consil',
            'cidade': {'nome': 'Cuiabá'},
            'estado': {'sigla': 'MT'},
        }

        requests_mock.get(TestCepaberto.FAKE_URL, json=fake_response, status_code=200)
        token = getenv('CEPABERTO_TOKEN') or None
        client = Cepaberto(ZIPCODE, token)
        error, result = client.search()
        return result

    def test_base_url(self):
        assert Cepaberto.API_URL == TestCepaberto.FAKE_BASE_URL

    def test_get_url(self):
        token = getenv('CEPABERTO_TOKEN') or None
        client = Cepaberto(ZIPCODE, token)
        assert client.get_url() == TestCepaberto.FAKE_URL

    def test_estado(self, cepaberto_success):
        assert cepaberto_success.get('data').get('state') == 'MT'

    def test_localidade(self, cepaberto_success):
        assert cepaberto_success.get('data').get('city') == 'Cuiabá'

    def test_bairro(self, cepaberto_success):
        assert cepaberto_success.get('data').get('district') == 'Consil'

    def test_endereco(self, cepaberto_success):
        address = 'Avenida Miguel Sutil, de 5799/5800 a 7887/7888'
        assert cepaberto_success.get('data').get('address') == address

    def test_invalid_zipcode(self):
        token = getenv('CEPABERTO_TOKEN') or None
        client = Cepaberto(INVALID_ZIPCODE, token)
        error, data = client.search()
        assert error is True

    def test_raises_zipcode_error(self):
        with pytest.raises(TokenError) as e:
            Cepaberto(ZIPCODE, '')

        assert e.value.args[0] == 'Token invalid.'
