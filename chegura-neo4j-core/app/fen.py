import falcon

from app.db import DB


class FenResource(object):
    def on_get_base(self, req, resp):
        all_fen = DB().get_all_fen_with_relations()
        resp.media = list(all_fen)

        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
