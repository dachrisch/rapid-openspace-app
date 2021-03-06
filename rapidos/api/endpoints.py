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

locations_model = api.model('Session Locations',
                            {
                                'id': String(readonly=True),
                                'name': String(required=True)
                            })


@ns.route('/')
class RapidosListResource(Resource):
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


@ns.route('/<rapidos_id>')
@ns.param('id', 'Rapidos identifier')
class RapidosResource(Resource):
    @ns.marshal_with(rapidos_model)
    def get(self, rapidos_id: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return rapidos_service.get(rapidos_id)


@ns.route('/<rapidos_id>/locations')
@ns.param('id', 'Rapidos identifier')
class SessionLocationListResource(Resource):
    @ns.expect(locations_model)
    @ns.marshal_with(locations_model)
    def post(self, rapidos_id: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        name = api.payload.get('name')
        return rapidos_service.add_session_location(name).to(rapidos_id), 201

    @ns.marshal_list_with(locations_model)
    def get(self, rapidos_id: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return list(rapidos_service.get_session_locations().of(rapidos_id))


@ns.route('/<rapidos_id>/locations/<location_id>')
@ns.param('id', 'Rapidos identifier')
class SessionLocationResource(Resource):
    @ns.marshal_with(locations_model)
    def get(self, rapidos_id: str, location_id: str,
            rapidos_service: RapidosService = Provide[Container.creation_service]):
        return next(
            filter(lambda location: location.id == location_id, rapidos_service.get_session_locations().of(rapidos_id)))

    def delete(self,rapidos_id: str, location_id: str,
            rapidos_service: RapidosService = Provide[Container.creation_service]):
        rapidos_service.remove_session_locations(location_id).of(rapidos_id)
        return 204