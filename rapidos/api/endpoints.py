from datetime import datetime, timedelta

from dependency_injector.wiring import Provide, inject
from flask_restx import Resource
from flask_restx.fields import String, DateTime, Integer

from rapidos import RapidosService, Container
from rapidos.api import api

ns = api.namespace('rapidos')

rapidos_model = api.model('Rapidos',
                          {
                              'id': String(readonly=True),
                              'name': String(required=True),
                              'start': DateTime(required=True),
                              'duration': Integer(required=True, description='Duration of one Session in Minutes'),
                              'sessions': Integer(required=True)}
                          )


@ns.route('/')
class RapidosResourceList(Resource):
    @inject
    @ns.expect(rapidos_model, validate=True)
    @ns.marshal_with(rapidos_model)
    def post(self, rapidos_service: RapidosService = Provide[Container.creation_service]):
        name = api.payload.get('name')
        start = datetime.fromisoformat(api.payload.get('start'))
        duration = timedelta(minutes=int(api.payload.get('duration')))
        sessions = api.payload.get('sessions', 1)
        uuid = rapidos_service.create(name, start, duration, sessions)
        return {
                   'id': uuid,
                   'name': name,
                   'start': start,
                   'duration': duration.total_seconds() / 60,
                   'sessions': sessions
               }, 201


@ns.route('/<uuid>')
@ns.param('id', 'Rapidos identifier')
class RapidosResource(Resource):
    @ns.marshal_with(rapidos_model)
    def get(self, uuid: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return rapidos_service.get(uuid)
