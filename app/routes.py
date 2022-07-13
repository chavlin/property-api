"""
Endpoints for the application are defined here.
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


# Let's make this a POST request to keep the address/zip slightly more secure; also makes access pattern in the URL easier to handle for consumer.
# If we wanted to coordinate with the Web App around "PropertyIDs" loaded from a centralized DB,
# that's another option; do a lookup and make the request to the 3rd party API accordingly.
@app.route('/v1/property/septic-status', methods=['POST'])
def get_septic_status():
    """
    Endpoint to get septic status.
    """
    app.logger.info('Querying septic status...')
    app.logger.info(request.form)
    HouseCanaryV2API.is_septic_system(address, zipcode)
    return Response('Just Testing!', status=200)
