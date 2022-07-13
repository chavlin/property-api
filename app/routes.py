"""
Endpoints for the application are defined here.
"""

import logging

import flask
from flask import Response

app = flask.Flask("property_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/v1/septic-status", methods=["GET"])
def get_septic_status():
    """
    Endpoint to get repository count for a Profile.
    """
    return Response("Just Testing!", status=200)
