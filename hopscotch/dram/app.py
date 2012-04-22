# Standard Library

# Third Party Libraries
from mongoalchemy.session import Session

# Local Libraries
from hopscotch.mongoapi.api import DocumentResource
from hopscotch.dram.documents import Drink
from hopscotch.dram.dram import Dram

dram = Dram(database = 'dram')
app = dram.dram

class DrinkResource(DocumentResource):
    document = Drink
    app = app

api = DrinkResource()
api.urls('v1')

if __name__ == '__main__':
    app.run(debug=True)