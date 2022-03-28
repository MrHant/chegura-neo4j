import falcon

from app.db import DB


class FenResource(object):
    def on_get_base(self, req, resp):
        all_fen = DB().get_all_fen_with_relations()
        resp.media = list(filter(lambda x: x is not None, all_fen))

        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200

    def on_get_data(self, req, resp):
        fen = req.get_param('fen')
        result = list(DB().get_fen_with_relations(fen))
        if len(result) == 0:
            resp.media = []
        else:
            r = result[0]
            resp.media = {
                'fen': r[0],
                'bestMove': r[1].get('bestMove'),
                'score': r[1].get('score'),
                'depth': r[1].get('depth'),
                'sp': int(r[1].get('score') * 100)
            }

        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200