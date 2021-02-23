from flask_restx import Resource

from rapidos.api import api

ns = api.namespace('v1')


@ns.route('/rapidos')
class RapidosResource(Resource):
    def post(self):
        return {}, 201
