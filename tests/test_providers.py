from os import getenv
import pytest
from dotenv import load_dotenv

from hub_cep.providers import Postmon, Viacep, Cepaberto


ZIPCODE = '78048000'
INVALID_ZIPCODE = '3111111'

load_dotenv()


class TestViacep:

    @pytest.fixture(scope='class')
    def data(self):
        client = Viacep(ZIPCODE)
        return client.search()

    def test_estado(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('state') == 'MT'

    def test_localidade(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('city') == 'Cuiabá'

    def test_bairro(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('district') == 'Alvorada'

    def test_endereco(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('address') == 'Avenida Miguel Sutil'

    def test_data_invalid(self):
        client = Viacep(INVALID_ZIPCODE)
        error, data = client.search()
        assert error is True


class TestPostmon:

    @pytest.fixture(scope='class')
    def data(self):
        client = Postmon(ZIPCODE)
        return client.search()

    def test_estado(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('state') == 'MT'

    def test_localidade(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('city') == 'Cuiabá'

    def test_bairro(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('district') == 'Alvorada'

    def test_endereco(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('address') == 'Avenida Miguel Sutil'

    def test_invalid_zipcode(self):
        client = Postmon(INVALID_ZIPCODE)
        error, data = client.search()
        assert error is True


class TestCepaberto:

    @pytest.fixture(scope='class')
    def data(self):
        token = getenv('CEPABERTO_TOKEN') or None
        client = Cepaberto(ZIPCODE, token)
        return client.search()

    def test_estado(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('state') == 'MT'

    def test_localidade(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('city') == 'Cuiabá'

    def test_bairro(self, data):
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('district') == 'Consil'

    def test_endereco(self, data):
        address = 'Avenida Miguel Sutil, de 5799/5800 a 7887/7888'
        if data[0] and data[1].get('timeout'):
            pytest.skip("Timeout raises")

        assert data[1].get('data').get('address') == address

    def test_invalid_zipcode(self):
        token = getenv('CEPABERTO_TOKEN') or None
        client = Cepaberto(INVALID_ZIPCODE, token)
        error, data = client.search()
        assert error is True
