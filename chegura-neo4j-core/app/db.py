from neo4j import GraphDatabase


class DB(object):
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j', 'password'))

    def close(self):
        self.driver.close()

    def get_all_fen_with_relations(self):
        with self.driver.session() as session:
            result = session.run("""
             MATCH (b:Board)-[r]->()
             WHERE r.evaluation_value <> ''
             RETURN DISTINCT b.fen as fen, collect(r) as moves
             """)
            for row in result:
                fen = row['fen']
                best_move = None
                for move in row['moves']:
                    if best_move is None or move.get('evaluation_value') >= best_move.get('evaluation_value'):
                        best_move = move

                if best_move.get('move') != '':
                    yield [fen, {
                        "bestMove": best_move.get('move'),
                        "score": best_move.get('evaluation_value'),
                        "depth": best_move.get('evaluation_depth')
                    }]

