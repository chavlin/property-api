import json

from app.models import HouseCanaryV2API


class TestHomeCanaryV2API():
    def test_property_details_endpoint(self, housecanary_property_details_response, requests_mock):
        """Mostly mocked but confirms no exceptions are triggered in the codepath."""
        api = HouseCanaryV2API()
        requests_mock.get(
            api.property_details_endpoint,
            text=json.dumps(housecanary_property_details_response),
            status_code=200,
        )

        response = api.get_property_details({'address': 'fake-address', 'zipcode': 'fake-zip'})

        # Check that data is formatted as expected:
        response_body = json.loads(response.text)
        assert api.get_sewer_type(response_body) == 'septic'

    def test_property_details_batch_endpoint(self, housecanary_property_details_batch_response, requests_mock):
        """Mostly mocked but confirms no exceptions are triggered in the codepath."""
        api = HouseCanaryV2API()
        requests_mock.post(
            api.property_details_endpoint,
            text=json.dumps(housecanary_property_details_batch_response),
            status_code=200,
        )

        response = api.get_property_details_batch(
            [
                {'address': 'fake-address', 'zipcode': 'fake-zip'},
                {'address': 'fake-address2', 'zipcode': '67890'}
            ]
        )

        response_body = json.loads(response.text)
        assert len(response_body) == 2
        assert api.get_sewer_type(response_body[0]) == 'septic'
        assert api.get_sewer_type(response_body[1]) == 'municipal'