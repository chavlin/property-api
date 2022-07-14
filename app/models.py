"""
Core models of the application are defined here.
"""
import requests


# Eventually we could store these parameters in AWS SSM or Secrets Manager; load them dynamically from the code.
HOUSE_CANARY_API_KEY = 'my-api-key'
HOUSE_CANARY_SECRET_KEY = 'my-secret-key'
HOUSE_CANARY_AUTH = (HOUSE_CANARY_API_KEY, HOUSE_CANARY_SECRET_KEY)


class HouseCanaryV2API():
    """HouseCanary v2 API implementation."""
    base_endpoint = 'https://api.housecanary.com/v2'
    property_details_endpoint = f'{base_endpoint}/property/details'

    def make_get_request(self, endpoint, params=None):
        """Wrapper function to handle GET requests from 3rd party API.
        Could perhaps move this to a base class if we had a different 3rd party API class in this service.
        """
        if not params:
            params = dict()

        response = requests.get(
            endpoint,
            params,
            auth=HOUSE_CANARY_AUTH,
            timeout=30
        )
        return response

    def make_post_request(self, endpoint, json=None):
        """Wrapper function to handle POST requests from 3rd party API.
        Could perhaps move this to a base class if we had a different 3rd party API class in this service.
        """
        if not json:
            json = dict()

        response = requests.post(
            endpoint,
            json=json,
            auth=HOUSE_CANARY_AUTH,
            timeout=30
        )
        return response

    def get_property_details(self, params: dict):
        """Access the GET property-details endpoint"""
        return self.make_get_request(self.property_details_endpoint, params)

    def get_property_details_batch(self, json: dict):
        """Access the POST property-details endpoint (batch mode)"""
        return self.make_post_request(self.property_details_endpoint, json)

    def get_sewer_type(self, property_details_response: dict):
        """Helper function to parse response from property-details endpoint to find the sewer system type."""
        return property_details_response['property/details']['result']['property']['sewer']
