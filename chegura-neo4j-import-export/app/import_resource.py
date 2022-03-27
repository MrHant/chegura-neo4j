import json
import falcon
import chess

from app.db import DB


class ImportResource(object):
    def on_post_upsert(self, req, resp):
        db = DB()

        def get_current_move(moves_payload):
            move = {
                "move": moves_payload.get('m'),
                "number": moves_payload.get('n'),
                "color": moves_payload.get('c'),
                "type": moves_payload.get('t'),
            }
            if moves_payload.get('e') is not None:
                move['evaluation_value'] = moves_payload.get('e').get('v')
                move['evaluation_depth'] = moves_payload.get('e').get('d')
            return move

        def parse(moves_payload, fen):
            current_move = get_current_move(moves_payload)
            move = current_move.get('move')

            # Prepare board with current move
            board = chess.Board(fen)
            if move != '':
                board.push_san(current_move.get('move'))
            next_fen = board.fen()

            # Add move into DB
            db.add_board(fen)
            db.add_board(next_fen)
            db.add_move(fen, current_move, next_fen)

            # Recursively parse next moves
            next_moves = moves_payload.get('s')
            for move in next_moves:
                parse(move, next_fen)

        try:
            payload = json.loads(req.stream.read())
        except:
            resp.status = falcon.HTTP_500
            return

        # Start parsing at initial board position
        parse(payload, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")

        resp.text = "Imported successfully"

        db.close()
        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
