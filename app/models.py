"""
Core models of the application are defined here.
"""

import logging

import flask
import requests


# Eventually we could store these parameters in AWS SSM or Secrets Manager; load them dynamically from the code.
HOUSE_CANARY_API_KEY = 'my-api-key'
HOUSE_CANARY_SECRET_KEY = 'my-secret-key'
HOUSE_CANARY_AUTH = (HOUSE_CANARY_API_KEY, HOUSE_CANARY_SECRET_KEY)

app = flask.Flask('property_api')
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


class HouseCanaryV2API():
    """HouseCanary v2 API implementation."""
    base_endpoint = 'https://api.housecanary.com/v2'
    property_details_endpoint = f"{base_endpoint}/property/details"

    # TODO let's support a get_ endpoint and a post_ endpoint, in case we want to grab batches...
    def make_get_request(self, endpoint, params=None):
        """Wrapper function to handle GET requests from 3rd party API.
        Could imagine moving this to a base class if we had a different 3rd party API class in this service.
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

    # This might be better placed in a View instead of the API Model, but was easier to set up testing this way:
    def is_septic_system(self, property_details_response: dict):
        sewer_type = property_details_response['property/details']['result']['property']['sewer']

        # NOTE: Endpoint can return any of the following: [Municipal, None, Storm, Septic, Yes]
        # 'Yes' denotes the possible existence of a Septic system; but for now endpoint will only return confirmation when we know for sure that Septic system exists.
        if sewer_type.lower() == 'septic':
            return True
        return False