from datetime import timedelta

from dependency_injector.wiring import inject, Provide
from flask import render_template, url_for
from flask_classful import FlaskView, route
from flask_wtf import FlaskForm, RecaptchaField
from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField

from rapidos import Container
from rapidos.service import RapidosService


class ServeView(FlaskView):
    route_base = '/rapidos'

    @inject
    def index(self, uuid: str, rapidos_service: RapidosService = Provide[Container.creation_service]):
        return render_template('serve.html', rapidos=rapidos_service.get(uuid))


class CreateView(FlaskView):
    route_base = '/rapidos'

    @inject
    @route('/create', methods=('GET', 'POST'))
    def create(self, rapidos_service: RapidosService = Provide[Container.creation_service]):
        form = CreateForm()
        if form.validate_on_submit():
            rapidos_id = rapidos_service.create(form.name_field.data, form.duration_selected(),
                                                form.sessions_selected())
            return redirect(url_for('ServeView:index', uuid=rapidos_id))
        return render_template('create.html', form=form)


class CreateForm(FlaskForm):
    sessions_field_options = {
        0: 1,
        1: 2,
        2: 3
    }

    duration_field_options = {
        0: ('30 Minuten', timedelta(minutes=30)),
        1: ('45 Minuten', timedelta(minutes=45)),
        2: ('60 Minuten', timedelta(minutes=60)),
        3: ('90 Minuten', timedelta(minutes=90)),
    }

    name_field = StringField(
        'Open Space Name'
    )
    sessions_field = SelectField(
        'Anzahl Sessions', choices=list(sessions_field_options.items())
    )
    duration_field = SelectField(
        'Sessionlänge', choices=[(entry, label_value[0]) for entry, label_value in duration_field_options.items()]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Erstellen')

    def sessions_selected(self):
        return self.sessions_field_options[int(self.sessions_field.data)]

    def duration_selected(self):
        return self.duration_field_options[int(self.duration_field.data)][1]
