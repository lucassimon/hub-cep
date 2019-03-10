from hub_cep.zipcode import ZipCode


def get_address(event, context):

    zipcode = event['path']['cep']

    client = ZipCode(zipcode)
    status_code, body = client.search()

    response = {
        "statusCode": status_code,
        "body": body
    }

    return response
