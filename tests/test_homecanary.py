import json

from app.models import HouseCanaryV2API

def test_property_details_endpoint_is_septic(housecanary_property_details_response, requests_mock):
    api = HouseCanaryV2API()

    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=200,
    )

    response = api.get_property_details('fake-address', 'fake-zip')
    
    # Check that data is formatted as expected:
    assert response.json()['property/details']['result']['property']['sewer'] == 'septic'

    assert api.is_septic_system(response.json())


def test_property_details_endpoint_is_not_septic(housecanary_property_details_response, requests_mock):
    # Change fixture to a non-septic setting
    housecanary_property_details_response['property/details']['result']['property']['sewer'] = 'municipal'

    api = HouseCanaryV2API()
    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=200,
    )

    response = api.get_property_details('fake-address', 'fake-zip')
    
    # Check that data is formatted as expected:
    assert response.json()['property/details']['result']['property']['sewer'] == 'municipal'

    assert not api.is_septic_system(response.json())
