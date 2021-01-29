from flask import render_template
from flask_classful import FlaskView, route


class CreateView(FlaskView):
    route_base = '/rapidos'

    @route('/create')
    def create(self):
        return render_template('create.html')
