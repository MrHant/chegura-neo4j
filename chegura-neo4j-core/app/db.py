from neo4j import GraphDatabase


class DB(object):
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j', 'password'))

    def close(self):
        self.driver.close()

    def _parse_fen_with_relations(self, row):
        fen = row['fen']
        best_move = None
        for move in row['moves']:
            if best_move is None or move.get('evaluation_value') >= best_move.get('evaluation_value'):
                best_move = move

        if best_move.get('move') != '':
            return [fen, {
                "bestMove": best_move.get('move'),
                "score": best_move.get('evaluation_value'),
                "depth": best_move.get('evaluation_depth')
            }]

    def get_fen_with_relations(self, fen):
        with self.driver.session() as session:
            result = session.run("""
             MATCH (b:Board {fen: $fen})-[r]->()
             WHERE r.evaluation_value <> ''
             RETURN DISTINCT b.fen as fen, collect(r) as moves
             """, fen=fen)
            for row in result:
                yield self._parse_fen_with_relations(row)

    def get_all_fen_with_relations(self):
        with self.driver.session() as session:
            result = session.run("""
             MATCH (b:Board)-[r]->()
             WHERE r.evaluation_value <> ''
             RETURN DISTINCT b.fen as fen, collect(r) as moves
             """)
            for row in result:
                yield self._parse_fen_with_relations(row)

