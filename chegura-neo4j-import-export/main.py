import falcon
from waitress import serve

from app.db import DB
from app.export_resource import ExportResource
from app.landing import LandingResource
from app.import_resource import ImportResource

api = application = falcon.App()
DB.init_db()

# Add routes
api.add_route('/', LandingResource())
import_resource = ImportResource()
api.add_route('/import/upsert', import_resource, suffix='upsert')
api.add_route('/export.json', ExportResource(), suffix='json')

# Start server
serve(api, listen='*:8100')
