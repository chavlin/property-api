"""
Endpoints for the application are defined here.

This structure is good for simple demo; as app grows in complexity
might prefer using Flask Blueprint for route structure which can
link directly to View functions imported elsewhere.
"""

import logging

import flask
from flask import Response, request

from .models import HouseCanaryV2API


app = flask.Flask('property_api')
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route('/health-check', methods=['GET'])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info('Health Check!')
    return Response('All Good!', status=200)


# Let's make this a POST request to keep the queried address/zip slightly more secure (won't appear in server logs)
# also makes access pattern in the URL easier to handle for consumer.
# If we wanted to coordinate with the Web App around "PropertyIDs" loaded from a centralized DB, that's another option.
# GET to /v1/property/{property_id}/septic-status triggers a lookup to a centralized DB or local cache for Address+zip lookup,
# then make the request to the 3rd party API accordingly.
@app.route('/v1/property/septic-status', methods=['POST'])
def get_septic_status():
    """
    Endpoint that returns whether a property has a septic system.
    Interfaces with the HouseCanary API, handling input construction and output parsing.
    """
    app.logger.info('Querying septic status...')

    request_body = request.get_json()
    app.logger.info(f'request_body: {request_body}')

    api = HouseCanaryV2API()

    response = api.get_property_details(
        request_body.get('address'),
        request_body.get('zipcode'),
    )

    if response.status_code != 200:
        logger.warning('3rd-party API returned non-200 response.', extra={'status_code': response.status_code, 'response_text': response.text})
        return Response('Error received from 3rd-party API. Check property-api logs for details.', 424)

    sewer_type = response['property/details']['result']['property']['sewer']

    # TODO Should I return responses as Property objects?  Let's wait until the unit test gets set up.
    # NOTE: Endpoint can return any of the following: [Municipal, None, Storm, Septic, Yes]
    # 'Yes' denotes the possible existence of a Septic system; but for now endpoint will only return confirmation when we know for sure that Septic system exists.
    if sewer_type == 'Septic':
        return Response('Septic system found.', 200)

    return Response('Septic system not found.', 200)
