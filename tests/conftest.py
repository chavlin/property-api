import pytest
from copy import deepcopy

from app.routes import create_app


@pytest.fixture()
def test_app():
    """This and the following fixture set up a mocked app server that can be used to call routes directly in unit tests."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def housecanary_property_details_response():
    return {
        "property/details": {
            "api_code_description": "ok",
            "api_code": 0,
            "result": {
                "property": {
                    "air_conditioning": "yes",
                    "attic": False,
                    "basement": "full_basement",
                    "building_area_sq_ft": 1824,
                    "building_condition_score": 5,
                    "building_quality_score": 3,
                    "construction_type": "Wood",
                    "exterior_walls": "wood_siding",
                    "fireplace": False,
                    "full_bath_count": 2,
                    "garage_parking_of_cars": 1,
                    "garage_type_parking": "underground_basement",
                    "heating": "forced_air_unit",
                    "heating_fuel_type": "gas",
                    "no_of_buildings": 1,
                    "no_of_stories": 2,
                    "number_of_bedrooms": 4,
                    "number_of_units": 1,
                    "partial_bath_count": 1,
                    "pool": True,
                    "property_type": "Single Family Residential",
                    "roof_cover": "Asphalt",
                    "roof_type": "Wood truss",
                    "site_area_acres": 0.119,
                    "style": "colonial",
                    "total_bath_count": 2.5,
                    "total_number_of_rooms": 7,
                    "sewer": "septic",
                    "subdivision" : "CITY LAND ASSOCIATION",
                    "water": "municipal",
                    "year_built": 1957,
                    "zoning": "RH1"
                },
                "assessment":{
                    "apn": "0000 -1111",
                    "assessment_year": 2015,
                    "tax_year": 2015,
                    "total_assessed_value": 1300000.0,
                    "tax_amount": 15199.86
                } 
            }
        }
    }


@pytest.fixture
def housecanary_property_details_batch_response(housecanary_property_details_response):
    property1 = deepcopy(housecanary_property_details_response)
    property2 = deepcopy(housecanary_property_details_response)

    property2['property/details']['result']['property']['sewer'] = 'municipal'

    return [
        property1,
        property2,
    ]