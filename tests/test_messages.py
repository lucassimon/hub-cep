from hub_cep.messages import Messages


def test_network_error():
    assert Messages.NETWORK_ERROR.name == 'NETWORK_ERROR'
    assert Messages.NETWORK_ERROR.value == 'Network error.'


def test_not_implemented():
    assert Messages.NOT_IMPLEMENTED.name == 'NOT_IMPLEMENTED'
    assert Messages.NOT_IMPLEMENTED.value == 'Should implement.'


def test_strange_error():
    assert Messages.STRANGE_ERROR.name == 'STRANGE_ERROR'
    assert Messages.STRANGE_ERROR.value == 'An error ocurred.'


def test_success():
    assert Messages.SUCCESS.name == 'SUCCESS'
    assert Messages.SUCCESS.value == 'Success.'


def test_token_invalid():
    assert Messages.TOKEN_INVALID.name == 'TOKEN_INVALID'
    assert Messages.TOKEN_INVALID.value == 'Token invalid.'


def test_zipcode_invalid():
    assert Messages.ZIPCODE_INVALID.name == 'ZIPCODE_INVALID'
    assert Messages.ZIPCODE_INVALID.value == 'Zipcode invalid.'


def test_zipcode_not_found():
    assert Messages.ZIPCODE_NOT_FOUND.name == 'ZIPCODE_NOT_FOUND'
    assert Messages.ZIPCODE_NOT_FOUND.value == 'Zip code not found.'
