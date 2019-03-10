import pytest
import requests

from hub_cep.zipcode import ZipCode, AbstractZipCode
from hub_cep.exceptions import ZipcodeError

from .test_providers import ZIPCODE, INVALID_ZIPCODE

MOCK_RESULT = {'error': False, 'message': 'Success.', 'data': {'zip_code': '78048-000', 'address': 'Avenida Miguel Sutil', 'number': '', 'info': '', 'district': 'Alvorada', 'city': 'Cuiabá', 'state': 'MT', 'country': 'BRA'}}


class TestAbstractZipcode:
    @pytest.fixture(scope='class')
    def data(self):
        obj = AbstractZipCode
        return obj

    def test_zipcode_setter(self, data):
        data.zipcode = ZIPCODE
        assert data.zipcode == ZIPCODE

    def test_raises_not_implemented_error_when_call_search_method(self, data):
        with pytest.raises(NotImplementedError) as e:
            data.search()

        assert e.value.args[0] == 'Should implement.'


class TestZipcode:

    def test_zipcode_getter(self):
        client = ZipCode(ZIPCODE)
        assert client.zipcode == ZIPCODE

    def test_zipcode_setter(self):
        client = ZipCode(ZIPCODE)
        client.zipcode = INVALID_ZIPCODE
        assert client.zipcode == INVALID_ZIPCODE

    def test_raises_zipcode_error_when_is_empty_string(self):
        with pytest.raises(ZipcodeError) as e:
            ZipCode('')

        assert e.value.args[0] == 'Zipcode invalid.'

    def test_raises_zipcode_error_when_is_none(self):
        with pytest.raises(ZipcodeError) as e:
            ZipCode(None)

        assert e.value.args[0] == 'Zipcode invalid.'

    def test_fetch_sucess(self):
        client = ZipCode(ZIPCODE)
        status_code, result = client.search()
        assert status_code == 200
        assert result == MOCK_RESULT

    def test_fetch_with_error(self):
        client = ZipCode(INVALID_ZIPCODE)
        status_code, result = client.search()

        if result.get('error') and result.get('timeout'):
            pytest.skip("Timeout raises")

        assert status_code == 422
        assert result == {'error': True, 'message': 'Zip code not found.'}
