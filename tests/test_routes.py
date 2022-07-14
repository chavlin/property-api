"""Catchall test file for route logic; would be broken out into individual files down the line."""
import json

from app.models import HouseCanaryV2API


def test_healthcheck(client):
    response = client.get('/health-check')
    assert response.text == 'All Good!'


def test_septic_status_true(client, housecanary_property_details_response, requests_mock):
    # Change fixture to septic setting as precondition:
    housecanary_property_details_response['property/details']['result']['property']['sewer'] = 'septic'

    address = 'fake-address'
    zipcode = '12345'

    api = HouseCanaryV2API()
    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=200,
    )

    response = client.post(
        '/v1/property/septic-status',
        json={
            'address': address,
            'zipcode': zipcode,
        }
    )
    expected = {
        'address': address,
        'zipcode': zipcode,
        'septic': True,
    }
    assert json.loads(response.text) == expected


def test_septic_status_false(client, housecanary_property_details_response, requests_mock):
    # Change fixture to a non-septic setting as precondition:
    housecanary_property_details_response['property/details']['result']['property']['sewer'] = 'municipal'

    address = 'fake-address'
    zipcode = '12345'

    api = HouseCanaryV2API()
    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=200,
    )

    # Now test the behavior:
    response = client.post(
        '/v1/property/septic-status',
        json={
            'address': address,
            'zipcode': zipcode,
        }
    )

    expected = {
        'address': address,
        'zipcode': zipcode,
        'septic': False,
    }

    assert json.loads(response.text) == expected


def test_septic_status_error_response_from_third_party(client, housecanary_property_details_response, requests_mock):
    # Change fixture to septic setting as precondition:
    housecanary_property_details_response['property/details']['result']['property']['sewer'] = 'septic'

    address = 'fake-address'
    zipcode = '12345'

    api = HouseCanaryV2API()
    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=502, # Bad gateway
    )

    response = client.post(
        '/v1/property/septic-status',
        json={
            'address': address,
            'zipcode': zipcode,
        }
    )

    assert json.loads(response.text) == {'message': 'Error received from 3rd-party API. Check property-api logs for details.'}


def test_septic_status_batch(client, housecanary_property_details_batch_response, requests_mock):
    # Adjust fixture as precondition: one septic, one non-septic sewer system.
    housecanary_property_details_batch_response[0]['property/details']['result']['property']['sewer'] == 'septic'
    housecanary_property_details_batch_response[1]['property/details']['result']['property']['sewer'] == 'municipal'

    address1 = 'fake-address'
    zipcode1 = '12345'

    address2 = 'fake-address2'
    zipcode2 = '67890'

    api = HouseCanaryV2API()
    requests_mock.post(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_batch_response),
        status_code=200,
    )

    # Now test the behavior:
    response = client.post(
        '/v1/property/septic-status/batch',
        json=[
            {
                'address': address1,
                'zipcode': zipcode1,
            },
            {
                'address': address2,
                'zipcode': zipcode2,
            },
        ]
    )
    
    expected = [
        {
            'address': address1,
            'zipcode': zipcode1,
            'septic': True,
        },
        {
            'address': address2,
            'zipcode': zipcode2,
            'septic': False,
        }
    ]

    assert json.loads(response.text) == expected

