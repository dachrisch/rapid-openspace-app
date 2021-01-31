from dependency_injector.wiring import inject, Provide
from flask import render_template, url_for
from flask_classful import FlaskView, route
from werkzeug.utils import redirect

from rapidos import Container
from rapidos.service import RapidosService
from rapidos.web.forms import CreateForm


class MarketplaceView(FlaskView):
    route_base = '/rapidos'

    @inject
    @route('/marketplace/<uuid>')
    def marketplace(self, uuid: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return render_template('marketplace.html', uuid=uuid, rapidos=rapidos_service.get(uuid))


class CreateView(FlaskView):
    route_base = '/rapidos'

    @inject
    @route('/create', methods=('GET', 'POST'))
    def create(self, rapidos_service: RapidosService = Provide[Container.creation_service]):
        form = CreateForm()
        if form.validate_on_submit():
            rapidos_id = rapidos_service.create(form.name_field.data, form.start_datetime(), form.duration_selected(),
                                                form.sessions_selected())
            return redirect(url_for('MarketplaceView:marketplace', uuid=rapidos_id))
        return render_template('create.html', form=form)


