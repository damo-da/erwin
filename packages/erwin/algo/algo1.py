from typing import Optional

from chess import Board, Outcome

from erwin.db import GameResult
from .db import get_result_from_db
from .helpers import WIN, DRAW, MAX_DEPTH, fix_outcome


def get_result(b: Board, depth=0, db_sess=None, cache=None) -> Optional[Outcome]:
    # Check if the position is in database
    if db_sess:
        r = get_result_from_db(b, db_sess)

        if r:
            return r

    if cache is None:
        cache = {}

    fen = b.fen()
    if fen in cache:
        return cache[fen]

    result = fix_outcome(b.outcome(claim_draw=True))

    if result is None:
        if depth >= MAX_DEPTH:
            return None

        # Let's run a DFS
        moves = list(b.legal_moves)
        can_win = False
        can_draw = False
        inconclusive = 0

        for move in moves:
            b.push(move)
            new_o = get_result(b, depth=depth + 1, db_sess=db_sess)
            b.pop()

            if new_o is None:
                inconclusive += 1
                continue

            if new_o.termination == WIN:
                if new_o.winner == b.turn:  # We win
                    can_win = True
                    break
            elif new_o.termination == DRAW:  # We draw
                can_draw = True

        if can_win:
            result = Outcome(termination=WIN, winner=b.turn)
        elif can_draw:
            result = Outcome(termination=DRAW, winner=None)
        elif inconclusive > 0:
            result = None
        else:
            result = Outcome(termination=WIN, winner=not b.turn)

    if db_sess and result is not None:
        db_obj = GameResult.from_board(b, result)
        db_sess.add(db_obj)

        db_sess.commit()

    cache[fen] = result

    return result
