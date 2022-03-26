import falcon
from waitress import serve

from app.landing import LandingResource
from app.import_resource import ImportResource

api = application = falcon.App()

# Add routes
api.add_route('/', LandingResource())
import_resource = ImportResource()
api.add_route('/import/upsert', import_resource, suffix='upsert')

# Start server
serve(api, listen='*:8100')
