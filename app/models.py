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

    # TODO let's support a get_ endpoint and a post_ endpoint, in case we want to grab batches...
    # TODO let's abstract away address+zip into a Property class...
    # TODO let's write unit tests...
    # TODO let's figure out auth...
    def get_property_details(self, address: str, zipcode: str):
        property_details_endpoint = f"{self.base_endpoint}/property/details"
        property_response = requests.get(
            property_details_endpoint,
            params={'address': address, 'zipcode': zipcode},
            auth=HOUSE_CANARY_AUTH,
            timeout=30,
        )
        if property_response.status == 200:
            return property_response.json()
        else:
            # TODO we need to figure out graceful error handling.  Coordinate with Web app to determine what response it expects.
            return {'message': 'Error contacting Property endpoint.'}

    def get_sewer_system(self, address: str, zipcode: str):
        """Returns a JSONized dict representing a Github Organization."""
        response = self.get_property_details(address, zipcode)
        sewer_type = response['property/details']['result']['property']['sewer']
        return sewer_type

    def is_septic_system(self, address: str, zipcode: str):
        """Returns True if the property has a septic system."""
        sewer_type = self.get_sewer_system(address, zipcode)
        if sewer_type == 'Septic':
            return True
        return False