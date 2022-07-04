from chess.variant import AntichessBoard
from solver.main import get_result
import pytest


def test_win_in_0() -> None:
    fen = "8/p7/8/8/8/8/8/8 w - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b)

    assert r.winner  # White wins


def test_loss_in_1() -> None:
    fen = "8/8/8/8/p7/1B6/8/8 b - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b)
    assert r.winner  # White wins

    fen = "8/8/8/8/p7/1B6/8/8 w - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b)

    assert r.winner is False  # Black wins


def test_loss_in_2() -> None:
    fen = "8/8/8/8/p7/B7/8/8 w - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b)
    assert r.winner is False  # White wins


def test_draw() -> None:
    fen = "8/8/3k4/8/8/2K5/8/8 w - - 0 1"

    b = AntichessBoard(fen=fen)
    r = get_result(b)

    assert r.winner is None  # It's a draw at best play


def test_db(db_sess) -> None:
    fen = "8/p7/8/8/8/8/8/8 w - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b, db_sess=db_sess)

    assert r.winner  # White wins
