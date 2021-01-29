from dependency_injector.wiring import inject, Provide
from flask import render_template, url_for
from flask_classful import FlaskView, route
from flask_wtf import FlaskForm, RecaptchaField
from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField

from rapidos.service import Container
from rapidos.service.create import RapidosCreationService


class ServeView(FlaskView):
    route_base = '/rapidos'

    def index(self, uuid: str):
        return render_template('serve.html')


class CreateView(FlaskView):
    route_base = '/rapidos'

    @inject
    @route('/create', methods=('GET', 'POST'))
    def create(self, creation_service: RapidosCreationService = Provide[Container.creation_service]):
        form = CreateForm()
        if form.validate_on_submit():
            rapidos_id = creation_service.create(form.name.data, form.count.data, form.length.data)
            return redirect(url_for('ServeView:index', uuid=rapidos_id))
        return render_template('create.html', form=form)


class CreateForm(FlaskForm):
    name = StringField(
        'Open Space Name'
    )
    count = SelectField(
        'Anzahl Sessions', choices=((1, '1'), (2, '2'))
    )
    length = SelectField(
        'Sessionlänge', choices=((0, '30 Minuten'), (1, '45 Minuten'), (2, '60 Minuten'))
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Erstellen')
