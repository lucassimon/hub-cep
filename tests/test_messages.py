from hub_cep.messages import Messages


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