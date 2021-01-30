from datetime import timedelta

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


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
        'Open Space Name', [DataRequired()]
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
