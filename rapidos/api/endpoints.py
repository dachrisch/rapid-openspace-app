from flask_restx import Resource

from rapidos.api import api

ns = api.namespace('rapidos')


@ns.route('/')
class RapidosResource(Resource):
    def post(self):
        return {}, 201
