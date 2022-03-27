import falcon
from waitress import serve

from app.landing import LandingResource

api = application = falcon.App()

# Add routes
api.add_route('/', LandingResource())

# Start server
serve(api, listen='*:8101')
