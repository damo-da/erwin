from typing import Optional

from chess import Outcome, Board, Termination

from erwin.db import GameResult, Session
from .helpers import DRAW


def get_result_from_db(board: Board, session=None) -> Optional[Outcome]:
    if session is None:
        session = Session()

    temp_ = GameResult.from_board(board, Outcome(termination=DRAW, winner=None))
    r = session.query(GameResult).filter(
        GameResult.turn == temp_.turn,
        GameResult.variant == temp_.variant,
        GameResult.board_pos == temp_.board_pos,
    ).first()

    if r is not None:
        return Outcome(
            termination=Termination[r.outcome_termination],
            winner=r.outcome_winner
        )
