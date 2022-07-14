"""
Endpoints for the application are defined here.

This structure is good for simple demo; as app grows in complexity
might prefer using Flask Blueprint for route structure which can
link directly to View functions imported elsewhere.
"""
import flask
import json
import logging
from copy import deepcopy

from flask import Response, request

from app.models import HouseCanaryV2API


def create_app():
    app = flask.Flask('property-api')
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
    # GET /v1/property/{property_id}/septic-status could trigger a lookup to a centralized DB or local cache.
    # We pull address+zip off the Property object, then make the request to the 3rd party API accordingly.
    # Much depends on what the "Property" Domain Model looks like for the web app.
    @app.route('/v1/property/septic-status', methods=['POST'])
    def get_septic_status():
        """
        Endpoint that returns whether a property has a septic system.
        Interfaces with the HouseCanary API, handling input construction and output parsing.

        Example JSON body:
        {
            "address": "123 Main St.",
            "zipcode": "12345"
        }

        Example JSON response:
        {
            "address": "123 Main St.",
            "zipcode": "12345",
            "septic": true,
        }
        """
        app.logger.info('Querying septic status...')

        request_body = request.get_json()
        app.logger.debug(f'request_body: {request_body}')

        address = request_body.get('address')
        zipcode = request_body.get('zipcode')

        # a schema could do this better, but quick validation that args are formatted basically right:
        assert len(request_body) == 2
        assert address
        assert zipcode
    
        api = HouseCanaryV2API()
        property_response = api.get_property_details(request_body)

        if property_response.status_code != 200:
            logger.warning('3rd-party API returned non-200 response.',
                extra={
                    'status_code': property_response.status_code,
                    'response_text': property_response.text
                }
            )
            # For now we'll return 200 since the property-api service is not at fault.  Can work with web app if they expect different code / response.
            return Response('Error received from 3rd-party API. Check property-api logs for details.', 200)

        sewer_type = api.get_sewer_type(property_response.json())

        # NOTE: Endpoint can return any of the following: [Municipal, None, Storm, Septic, Yes]
        # 'Yes' denotes the possible existence of a Septic system; but for now endpoint will only return confirmation when we know for sure that Septic system exists.
        septic = False
        if sewer_type.lower() == 'septic':
            septic = True
  
        # Could codify these responses as Property objects, expanded as needed, potentially pulling much more data from the 3rd party api.
        final_response_body = {
            'address': address,
            'zipcode': zipcode,
            'septic': septic,
        }

        return Response(json.dumps(final_response_body), 200)

    @app.route('/v1/property/septic-status/batch', methods=['POST'])
    def get_septic_status_batch():
        """
        Batch endpoint that returns whether multiple properties have septic systems.
        Interfaces with the HouseCanary API, handling input construction and output parsing.

        Example JSON body:
        [
            {
                "address": "123 Main St.",
                "zipcode": "12345"
            },
            {
                "address": "456 Oak Pl.",
                "zipcode": "67890"
            }
        ]

        Example JSON response:
        [
            {
                "address": "123 Main St.",
                "zipcode": "12345",
                "septic": true,
            },
            {
                "address": "456 Oak Pl.",
                "zipcode": "67890",
                "septic": false
            }
        ]
        """
        app.logger.info('Querying septic status...')

        request_body = request.get_json()
        app.logger.debug(f'request_body: {request_body}')

        # a schema could do this better, but quick validation that args are formatted basically right:
        for property in request_body:
            assert len(property) == 2
            assert property.get('address')
            assert property.get('zipcode')
        
        api = HouseCanaryV2API()
        property_response = api.get_property_details_batch(request_body)

        if property_response.status_code != 200:
            logger.warning(
                '3rd-party API returned non-200 response.',
                extra={
                    'status_code': property_response.status_code,
                    'response_text': property_response.text
                }
            )
            return Response('Error received from 3rd-party API. Check property-api logs for details.', 200)

        # Here we will be savvier about forming the final response, using the response body as an initial template.
        # Then we merge septic information from the 3rd party API's property_response, one-by-one
        property_response_body = property_response.json()
        final_response_body = deepcopy(request_body)
        for i, property in enumerate(property_response_body):
            # NOTE: see above note on 'Yes' sewer systems; current implementation does NOT consider 'Yes' systems to be septic systems.
            if api.get_sewer_type(property).lower() == 'septic':
                final_response_body[i].update({'septic': True})
            else:
                final_response_body[i].update({'septic': False})

        return Response(json.dumps(final_response_body), 200)

    return app