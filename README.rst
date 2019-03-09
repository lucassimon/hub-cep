hub-cep
=======

Busca CEP utilizando diferentes provedores de consulta

.. image:: https://badge.fury.io/py/hub-cep.svg
    :target: https://badge.fury.io/py/hub-cep
    :alt: PyPI version

.. image:: https://circleci.com/gh/lucassimon/hub-cep.svg?style=svg
    :target: https://circleci.com/gh/lucassimon/hub-cep
    :alt: Build Status

.. image:: ./static/coverage.svg
    :alt: Code coverage Status

.. code-block:: python

    import json
	from hub_cep.zipcodes import ZipCode

    client = ZipCode(ZIPCODE)
    status_code, body = client.search()

    response = {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

    return response


Installing hub-cep
------------------

.. code-block:: bash

    pip install hub-cep
