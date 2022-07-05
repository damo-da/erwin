from chess import SQUARES, Move, Piece

from solver import Resolver


def empty_board():
    return list(" " * 64)


# def get_fen(board: list[str]):

def test_two_knights():
    from chess.variant import AntichessBoard

    # board = empty_board()

    m = Move.from_uci("e2e3")

    white_knight = Piece.from_symbol("N")
    black_knight = Piece.from_symbol("n")

    board = AntichessBoard(fen=None)
    board.set_piece_at(SQUARES[0], white_knight)
    board.set_piece_at(SQUARES[1], black_knight)
    # board2 = AntichessBoard()

    for sq1 in range(64):
        for sq2 in range(64):
            if sq1 == sq2:
                continue

            # set up
            board.set_piece_at(sq1, white_knight)
            board.set_piece_at(sq2, black_knight)

            this_fen = board.fen()
            Resolver().get_result(starting_fen=this_fen)

            # clean up
            board.remove_piece_at(sq1)
            board.remove_piece_at(sq2)
            break
        break

    print("Hi")
