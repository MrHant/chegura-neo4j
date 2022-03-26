import falcon


class LandingResource(object):
    def on_get(self, req, resp):
        resp.body = """
        # Import or Export DB data               
        """

        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
