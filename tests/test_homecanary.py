import json

from app.models import HouseCanaryV2API
from app.routes import get_septic_status

def test_property_details_endpoint(housecanary_property_details_response, requests_mock):
    api = HouseCanaryV2API()

    requests_mock.get(
        api.property_details_endpoint,
        text=json.dumps(housecanary_property_details_response),
        status_code=200,
    )

    response = api.get_property_details('fake-address', 'fake-zip')
    
    # Check that data is formatted as expected:
    assert response.json()['property/details']['result']['property']['sewer'] == 'septic'

    get_septic_status()