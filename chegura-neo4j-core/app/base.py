import falcon
import requests as requests


class BaseResource(object):
    def on_get_base(self, req, resp):
        proxied = requests.get('http://localhost:8100/export.json')
        resp.text = proxied.text

        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
