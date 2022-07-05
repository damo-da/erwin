from collections import defaultdict
from typing import Optional

from chess import Outcome
from chess.variant import AntichessBoard
from sqlalchemy import and_, or_

from .db import get_result_from_db
from .helpers import fix_outcome, WIN, DRAW, LOSS
from ..db import Session, GameResult

FEN = str


class Resolver:
    def __init__(self) -> None:
        self.results: dict[FEN, Optional[Outcome]] = defaultdict(lambda: None)
        self.parents: dict[FEN, set[FEN]] = defaultdict(set)

        self.sess = Session()

    def get_sub_results(self, node: FEN) -> dict[str, int]:
        sub_results = {"win": 0, "draw": 0, "lose": 0, "inconclusive": 0}
        board = AntichessBoard(fen=node)
        for child in get_children(node):
            if self.results[child] is None:
                sub_results["inconclusive"] += 1
            elif self.results[child].winner is None:
                sub_results["draw"] += 1
            elif self.results[child].winner is board.turn:
                sub_results["win"] += 1
            else:
                sub_results["lose"] += 1

        return sub_results

    def propagate(self, node: FEN):
        print(f"Back propagation for {node}.")

        pool = {node}
        while pool:
            new_pool = set()

            for node in sorted(pool):
                this_parents = self.parents[node]
                if self.results[node] is not None:
                    # This parent is already resolved. Forward propagate
                    new_pool.update(this_parents)
                    continue

                sub_results = self.get_sub_results(node)

                board = AntichessBoard(fen=node)

                if sub_results["win"] > 0:
                    # There is a way to win this line
                    self.results[node] = Outcome(termination=WIN, winner=board.turn)
                elif sub_results["draw"] > 0 and sub_results["inconclusive"] == 0:
                    self.results[node] = Outcome(termination=DRAW, winner=None)
                elif sub_results["lose"] > 0 and sub_results["inconclusive"] == 0:
                    self.results[node] = Outcome(termination=LOSS, winner=not board.turn)
                else:
                    # Still inconclusive. Stopping back propagation.
                    # print(f"Still inconclusive: {node}\t{sub_results}")
                    continue

                new_pool.update(this_parents)

            pool = new_pool

    def write_to_db(self) -> None:
        # Write results to database
        print("Identifying new writes.")

        all_grs = {}

        or_clause = []
        for node, r in self.results.items():
            if r is None:
                continue

            board = AntichessBoard(fen=node)
            gr = GameResult.from_board(board=board, outcome=r)

            or_clause.append(
                and_(GameResult.variant == gr.variant, GameResult.turn == gr.turn, GameResult.board_pos == gr.board_pos)
            )

            all_grs[(gr.variant, gr.board_pos, gr.turn)] = gr
        g = or_(*or_clause)
        existing = self.sess.query(GameResult).filter(g).all()

        for e in existing:
            del all_grs[(e.variant, e.board_pos, e.turn)]

        self.sess.add_all(all_grs.values())
        self.sess.commit()

    def get_result(self, starting_fen: FEN) -> Optional[Outcome]:
        pool: set[FEN] = {starting_fen}
        depth = 0

        while pool and not self.results[starting_fen]:
            print(f"Depth: {depth}, turn: {AntichessBoard(list(pool)[0]).turn}")

            new_pool: set[FEN] = set()

            for node in sorted(pool):
                if self.results[node]:
                    continue

                outcome = get_node_result(node, db_sess=self.sess)

                self.results[node] = outcome

                if outcome is None:
                    for child in get_children(node):
                        self.parents[child].add(node)

                        if child in self.results:
                            continue
                        self.results[child] = None
                        new_pool.add(child)

                else:
                    # Perform back propagation
                    self.propagate(node)

            depth += 1

            pool.clear()
            for node in new_pool:
                if not self.results[node]:
                    pool.add(node)

        self.write_to_db()

        return self.results[starting_fen]


def get_children(fen: FEN) -> set[FEN]:
    this_b = AntichessBoard(fen)

    child_fens = set()
    for m in this_b.legal_moves:
        this_b.push(m)
        child_fen = this_b.fen()
        this_b.pop()

        child_fens.add(child_fen)

    return child_fens


def get_node_result(fen: FEN, db_sess=None) -> Optional[Outcome]:
    board = AntichessBoard(fen=fen)

    outcome = fix_outcome(board.outcome(claim_draw=True))

    if outcome is None:
        # Try get from database
        outcome = get_result_from_db(board, session=db_sess)

    return outcome
