import pytest

from hub_cep.zipcode import ZipCode

from .test_providers import ZIPCODE, INVALID_ZIPCODE

MOCK_RESULT = {'error': False, 'message': 'Success.', 'data': {'zip_code': '78048-000', 'address': 'Avenida Miguel Sutil', 'number': '', 'info': '', 'district': 'Alvorada', 'city': 'Cuiabá', 'state': 'MT', 'country': 'BRA'}}


class TestZipcode:

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
