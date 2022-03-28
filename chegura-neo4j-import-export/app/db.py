from neo4j import GraphDatabase


def _parse_move(record):
    move = {
        'm': record.get('move'),
        'n': record.get('number'),
        'c': record.get('color')
    }
    if record.get('type') != '':
        move['t'] = record.get('type')
    if record.get('evaluation_value') != '':
        move['e'] = {
            'v': record.get('evaluation_value'),
            'd': record.get('evaluation_depth')
        }
    return move


class DB(object):
    @classmethod
    def init_db(cls):
        cls.driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j', 'password'))

    @classmethod
    def add_board(cls, fen):
        with cls.driver.session() as session:
            session.run("MERGE (a:Board {fen: $fen})", fen=fen)

    @classmethod
    def add_move(cls, fen, move, next_fen):
        with cls.driver.session() as session:
            session.run("""
            MATCH
              (prev:Board {fen: $fen}),
              (next:Board {fen: $next_fen})
            MERGE (prev)-[r:MOVE {move: $move, number: $number, color: $color, 
            type: $type_value, evaluation_value: $evaluation_value, evaluation_depth: $evaluation_depth}]->(next)
            """,
                        fen=fen, next_fen=next_fen, move=move.get('move'), number=move.get('number'),
                        color=move.get('color'), type_value=move.get('type') if move.get('type') is not None else '',
                        evaluation_value=move.get('evaluation_value', ""),
                        evaluation_depth=move.get('evaluation_depth', ""))

    @classmethod
    def get_moves(cls, fen):
        with cls.driver.session() as session:
            result = session.run("""
             MATCH (n:Board)-[r]->(x) where n.fen=$fen RETURN r as move
             """,
                                 fen=fen)
            for row in result:
                yield _parse_move(row['move'])

    @classmethod
    def get_all_moves(cls):
        with cls.driver.session() as session:
            result = session.run("""
             MATCH (n:Board)-[r:MOVE]->() RETURN n.fen as fen, collect(r) as moves
             """)
            for row in result:
                moves = []
                for record in row['moves']:
                    moves.append(_parse_move(record))
                yield row['fen'], moves
