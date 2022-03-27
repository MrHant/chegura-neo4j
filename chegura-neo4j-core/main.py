import falcon
from waitress import serve

from app.base import BaseResource
from app.fen import FenResource
from app.landing import LandingResource

api = application = falcon.App()

# Add routes
api.add_route('/', LandingResource())
api.add_route('/api/base', BaseResource(), suffix='base')
fen_resource = FenResource()
api.add_route('/api/fenbase', fen_resource, suffix='base')

# Start server
serve(api, listen='*:8101')
