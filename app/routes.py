"""
Endpoints for the application are defined here.

This structure is good for simple demo; as app grows in complexity
might prefer using Flask Blueprint for route structure which can
link directly to View functions imported elsewhere.
"""
import flask
import json
import logging
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

        Example body:
        {
            "address": "123 Main St.",
            "zipcode": "12345"
        }
        """
        app.logger.info('Querying septic status...')

        request_body = request.get_json()
        app.logger.info(f'request_body: {request_body}')

        address = request_body.get('address')
        zipcode = request_body.get('zipcode')
        
        api = HouseCanaryV2API()
        response = api.get_property_details(
            address,
            zipcode,
        )

        if response.status_code != 200:
            logger.warning('3rd-party API returned non-200 response.', extra={'status_code': response.status_code, 'response_text': response.text})
            # For now we'll return 200 since the property-api service is not at fault.  Can work with web app if they expect different code / response.
            return Response('Error received from 3rd-party API. Check property-api logs for details.', 200)

        sewer_type = response.json()['property/details']['result']['property']['sewer']

        # NOTE: Endpoint can return any of the following: [Municipal, None, Storm, Septic, Yes]
        # 'Yes' denotes the possible existence of a Septic system; but for now endpoint will only return confirmation when we know for sure that Septic system exists.
        septic = False
        if sewer_type.lower() == 'septic':
            septic = True
  
        # Could codify these responses as Property objects, expanded as needed, potentially pulling much more data from the 3rd party api.
        resp = {
            'address': address,
            'zipcode': zipcode,
            'septic': septic,
        }

        return Response(json.dumps(resp), 200)

    # @app.route('/v1/property/septic-status/batch', methods=['POST'])
    # def get_batch_septic_status():
    #     """
    #     Batch endpoint that returns whether multiple properties have septic systems.
    #     Interfaces with the HouseCanary API, handling input construction and output parsing.

    #     Example body:
    #     [
    #         {
    #             "address": "123 Main St.",
    #             "zipcode": "12345"
    #         }
    #     """
    #     app.logger.info('Querying septic status...')

    #     request_body = request.get_json()
    #     app.logger.info(f'request_body: {request_body}')

    #     api = HouseCanaryV2API()

    #     response = api.get_property_details(
    #         request_body.get('address'),
    #         request_body.get('zipcode'),
    #     )

    #     if response.status_code != 200:
    #         logger.warning('3rd-party API returned non-200 response.', extra={'status_code': response.status_code, 'response_text': response.text})
    #         # For now we'll return 200 since the property-api service is not at fault.  Can work with web app if they expect different code / response.
    #         return Response('Error received from 3rd-party API. Check property-api logs for details.', 200)

    #     sewer_type = response.json()['property/details']['result']['property']['sewer']

    #     # NOTE: Endpoint can return any of the following: [Municipal, None, Storm, Septic, Yes]
    #     # 'Yes' denotes the possible existence of a Septic system; but for now endpoint will only return confirmation when we know for sure that Septic system exists.
    #     if sewer_type.lower() == 'septic':
    #         resp = {'septic': True}
    #         return Response(json.dumps(resp), 200)

    #     # We could change response to be something like a Property object.  E.g. send back {'address': address, 'zipcode': zipcode, 'septic': True/False}
    #     # and any other data that could help the web app answer questions from the 3rd party API.
    #     resp = {'septic': False}
    #     return Response(json.dumps(resp), 200)

    return app