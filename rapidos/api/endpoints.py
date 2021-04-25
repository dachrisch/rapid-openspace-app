from datetime import datetime, timedelta

from dependency_injector.wiring import Provide, inject
from flask_restx import Resource
from flask_restx.fields import String, DateTime, Integer

from rapidos import RapidosService, Container
from rapidos.api import api
from rapidos.entity import Room

ns = api.namespace('rapidos')

rapidos_model = api.model('Rapidos',
                          {
                              'id': String(readonly=True),
                              'name': String(required=True),
                              'start': DateTime(required=True),
                              'duration': Integer(required=True, description='Duration of one Session in Minutes'),
                              'sessions': Integer(required=True)}
                          )

room_model = api.model('Rooms',
                       {
                           'id': String(readonly=True),
                           'name': String(required=True)
                       })


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
        rapidos = rapidos_service.create(name, start, duration, sessions)
        return rapidos, 201


@ns.route('/<uuid>')
@ns.param('id', 'Rapidos identifier')
class RapidosResource(Resource):
    @ns.marshal_with(rapidos_model)
    def get(self, uuid: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return rapidos_service.get(uuid)


@ns.route('/<rapidos_id>/rooms')
@ns.param('id', 'Rapidos identifier')
class RoomsResource(Resource):
    @ns.expect(room_model)
    @ns.marshal_with(room_model)
    def post(self, rapidos_id: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        name = api.payload.get('name')
        room = rapidos_service.add_room(name).to(rapidos_id)
        return room, 201
