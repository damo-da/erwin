from chess import Board, Outcome, Termination
from typing import Optional, Union
from solver.db import GameResult

WIN = Termination.VARIANT_WIN
DRAW = Termination.VARIANT_DRAW
LOSS = Termination.VARIANT_LOSS

MAX_DEPTH = 6


def fix_outcome(o: Optional[Outcome]) -> Optional[Outcome]:
    if o is None: return None

    if o.termination == LOSS:
        o.termination = WIN
        o.winner = not o.winner

    elif o.termination in (Termination.INSUFFICIENT_MATERIAL, Termination.THREEFOLD_REPETITION):
        o.termination = DRAW

    if o.termination not in (WIN, DRAW):
        raise Exception("Unknown outcome", o)

    return o


def get_result(b: Board, depth=0, db_sess=None, cache=None) -> Optional[Outcome]:
    # Check if the position is in database
    if db_sess:
        temp_ = GameResult.from_board(b, Outcome(termination=DRAW, winner=None))
        r = db_sess.query(GameResult).filter(
            GameResult.turn == temp_.turn,
            GameResult.variant == temp_.variant,
            GameResult.board_pos == temp_.board_pos,
        ).first()

        if r is not None:
            return Outcome(
                termination=Termination[r.outcome_termination],
                winner=r.outcome_winner
            )

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
