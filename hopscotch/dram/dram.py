import os
import json

from flask import (Flask, 
                    render_template)
from flask.views import View
from mongoalchemy.session import Session

session = Session.connect('dram')

dirname = os.path.dirname
PROJECT_ROOT = os.path.abspath(os.path.join(dirname(__file__),"..",".."))

# Get config
with open('%s/hopscotch/dram/config.json' % PROJECT_ROOT,'rb') as config_file:
    config = json.loads(config_file.read())

# Instantiate Flask Object
dram = Flask(__name__)
# Add the configuration vars into the jinja environment
dram.jinja_env.globals.update({
    'js': config['js'],
    'css': config['css'],
    'static_url': config['static_url']
})
# Instantiate jinja environment
dram.create_jinja_environment()

class BaseView(View):
    methods         = ['GET']


class Home(BaseView):
    def dispatch_request(self):
        return render_template('home.html')

class Checkin(BaseView):
    def dispatch_request(self):
        return render_template('checkin.html')

class Cabinet(BaseView):
    def dispatch_request(self):
        return render_template('cabinet.html')
    
dram.add_url_rule('/', view_func=Home.as_view('home_view'))
dram.add_url_rule('/checkin/', view_func=Home.as_view('checkin_view'))
dram.add_url_rule('/cabinet/', view_func=Home.as_view('cabinet_view'))


if __name__ == '__main__':
    dram.run(debug=True)