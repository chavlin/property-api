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

    def get_property_details(self, address: str, zipcode: str):
        params = {'address': address, 'zipcode': zipcode}
        return self.make_get_request(self.property_details_endpoint, params)
