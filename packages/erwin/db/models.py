from chess import Board, Outcome, Termination
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import declarative_base

from .engine import engine

terms_ = [e.name for e in Termination]
DbOutcomeTermination = Enum(*terms_, name="outcome_termination")

Base = declarative_base(bind=engine)
Base.metadata.create_all(engine)


class GameResult(Base):
    __tablename__ = "game_results"

    variant = Column(String(15), primary_key=True)
    board_pos = Column(String(300), primary_key=True)
    turn = Column(Boolean, primary_key=True)

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

    @property
    def outcome(self) -> Outcome:
        return Outcome(winner=self.outcome_winner, termination=Termination[self.outcome_termination])


class JobResult(Base):
    __tablename__ = "job_results"

    variant = Column(String(15), primary_key=True)
    board_pos = Column(String(300), primary_key=True)
    turn = Column(Boolean, primary_key=True)
