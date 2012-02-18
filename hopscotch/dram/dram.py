import os
import json

from flask import Flask, render_template
from mongoalchemy.session import Session

dram_session = Session('dram')

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

# Home
@dram.route('/')
def index():
    return render_template('home.html')
    
if __name__ == '__main__':
    dram.run(debug=True)