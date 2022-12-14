from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource
from jsonschema import validate

from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

logistics_status_namespace = Namespace('logistics_status', description='Logistics Status Namespace')


@logistics_status_namespace.route("/logistics/v1/on_status")
class OnInit(Resource):
    path_schema = get_json_schema_for_given_path('/on_status', domain="logistics")

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_status', domain="logistics")
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        validate(resp, response_schema)
        return resp

