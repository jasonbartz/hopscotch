# Third Party Libraries
from flask import render_template
from flask.views import View


class BaseView(View):
    methods         = ['GET']

class Home(BaseView):
    def dispatch_request(self):
        return render_template('home.html')

class Checkin(BaseView):
    def dispatch_request(self):
        return render_template('checkin.html')

class Cellar(BaseView):
    def dispatch_request(self):
        return render_template('cellar.html')

