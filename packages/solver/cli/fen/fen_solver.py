import click
from chess import Board
from chess.variant import AntichessBoard

from solver.algo import Resolver
from solver.algo.helpers import print_result
from ..options import OPTION_VARIANT, OPTION_VERBOSE, OPTION_FEN


@click.command()
@click.argument("fen", **OPTION_FEN)
@click.option("--variant", **OPTION_VARIANT)
@click.option("--verbose", **OPTION_VERBOSE)
def solver(fen: str, variant: str, verbose: bool = True):
    """Solve a given FEN."""

    if verbose:
        click.echo("Solving FEN")

        board: Board
        if variant == "antichess":
            board = AntichessBoard(fen)
        else:
            click.echo(f"Unknown variant: {variant}.", err=True)
            return exit(2)

        click.echo(board)
        click.echo()

    result = Resolver(verbose=verbose).get_result(starting_fen=fen)

    print_result(result)


if __name__ == "__main__":
    solver()
