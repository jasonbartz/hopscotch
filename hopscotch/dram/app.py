# Standard Library

# Third Party Libraries
from mongoalchemy.session import Session

# Local Libraries
from hopscotch.dram.api import DocumentResource
from hopscotch.dram.documents import Drink
from hopscotch.dram.dram import Dram

dram = Dram(database = 'dram')
app = dram.dram

# Need to figure this bit out
class DrinkResource(DocumentResource):
    document = Drink
    session = dram.session
    app = app

api = DrinkResource()
api.urls('v1')

if __name__ == '__main__':
    app.run(debug=True)