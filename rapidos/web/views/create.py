from flask import render_template, url_for
from flask_classful import FlaskView, route
from flask_wtf import FlaskForm, RecaptchaField
from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField


class CreateView(FlaskView):
    route_base = '/rapidos'

    @route('/create', methods=('GET', 'POST'))
    def create(self):
        form = CreateForm()
        if form.validate_on_submit():
            return redirect(url_for('ServeView:index'))
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
