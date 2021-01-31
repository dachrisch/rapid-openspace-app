from flask_restx import Resource

from rapidos.api import api

ns = api.namespace('marketplace')

@ns.route('/<string:marketplace_id>')
class Marketplace(Resource):

    def get(self, marketplace_id: str):
        return [{
                "slot": "13:00",
                "topic": "Thema 1"
            }]
