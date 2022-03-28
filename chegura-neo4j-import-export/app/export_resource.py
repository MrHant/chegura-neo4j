import falcon
import chess

from app.db import DB


class ExportResource(object):
    def on_get_json(self, req, resp):
        moves = dict(DB.get_all_moves())

        def get_moves(fen):
            next_moves = moves.get(fen)
            if next_moves is None:
                return []

            for move in next_moves:
                board = chess.Board(fen)
                if move.get('m') != '':
                    board.push_san(move.get('m'))
                next_fen = board.fen()
                move['s'] = get_moves(next_fen)

            return next_moves

        resp.media = get_moves("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")[0]

        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
