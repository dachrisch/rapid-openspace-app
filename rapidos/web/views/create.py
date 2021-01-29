from flask import render_template
from flask_classful import FlaskView


class CreateView(FlaskView):
    route_base = '/create'

    def index(self):
        return render_template('create.html')
