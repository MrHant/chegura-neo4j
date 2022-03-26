from neo4j import GraphDatabase


class DB(object):
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j', 'password'))

    def close(self):
        self.driver.close()

    def add_board(self, fen):
        with self.driver.session() as session:
            session.run("MERGE (a:Board {fen: $fen})", fen=fen)

    def add_move(self, fen, move, next_fen):
        with self.driver.session() as session:
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
