import json

from app.models import HouseCanaryV2API


class TestHomeCanaryV2API():
    def test_property_details_endpoint_is_septic(self, housecanary_property_details_response, requests_mock):
        """Mostly mocked but confirms no exceptions are triggered in the codepath."""
        api = HouseCanaryV2API()

        requests_mock.get(
            api.property_details_endpoint,
            text=json.dumps(housecanary_property_details_response),
            status_code=200,
        )

        response = api.get_property_details('fake-address', 'fake-zip')

        # Check that data is formatted as expected:
        assert response.json()['property/details']['result']['property']['sewer'] == 'septic'
