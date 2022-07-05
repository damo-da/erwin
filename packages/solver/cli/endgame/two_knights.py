import click
from chess import Piece, SQUARES, SQUARE_NAMES
from chess.variant import AntichessBoard

from solver.algo import Resolver
from solver.algo.helpers import print_result
from ..options import OPTION_VARIANT


@click.command()
@click.option("--variant", **OPTION_VARIANT)
def two_knights(variant: str = "antichess"):
    """Solve a two piece FEN."""

    white_knight = Piece.from_symbol("N")
    black_knight = Piece.from_symbol("n")

    board = AntichessBoard(fen=None)

    for sq1 in SQUARES:
        for sq2 in SQUARES:
            if sq1 == sq2:
                continue

            print(f"White knight: {SQUARE_NAMES[sq1]}, Black knight: {SQUARE_NAMES[sq2]}")

            # set up
            board.set_piece_at(sq1, white_knight)
            board.set_piece_at(sq2, black_knight)

            this_fen = board.fen()
            result = Resolver().get_result(starting_fen=this_fen)

            print_result(result)

            # clean up
            board.remove_piece_at(sq1)
            board.remove_piece_at(sq2)

            print()
            # break
        # break


if __name__ == "__main__":
    two_knights()
