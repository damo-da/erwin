from typing import Optional

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, Enum

from chess import Board, Outcome, Termination

Base = declarative_base()

terms_ = [e.name for e in Termination]
DbOutcomeTermination = Enum(*terms_, name="outcome_termination")


class GameResult(Base):
    __tablename__ = "game_results"

    variant = Column(String(15), primary_key=True, not_null=True)
    board_pos = Column(String(300), primary_key=True, not_null=True)
    turn = Column(Boolean, not_null=True, primary_key=True)

    outcome_termination = Column(DbOutcomeTermination)
    outcome_winner = Column(Boolean)

    @staticmethod
    def from_board(board: Board, outcome: Outcome) -> "GameResult":
        fen = board.fen()

        board_pos, turn, *_ = fen.split(" ")

        return GameResult(variant=board.uci_variant,
                          turn=board.turn,
                          outcome_termination=outcome.termination.name,
                          outcome_winner=outcome.winner,
                          board_pos=board_pos)
