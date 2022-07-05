from chess.variant import AntichessBoard
from erwin.main import get_result


# @pytest.mark("populator")
def test_populate_db(db_sess) -> None:
    fen = "8/8/3k4/8/8/2K5/8/8 w - - 0 1"
    b = AntichessBoard(fen=fen)
    r = get_result(b, db_sess=db_sess)

    assert r is None
