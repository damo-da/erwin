import click
from chess import Board
from chess.variant import AntichessBoard

from solver.algo import get_result
from .options import OPTION_FEN


@click.command()
@click.option("--fen", **OPTION_FEN)
def solver(fen: str, variant: str = "antichess"):
    """Solve a given FEN."""

    board: Board
    if variant == "antichess":
        board = AntichessBoard(fen)
    else:
        click.echo(f"Unknown variant: {variant}.", err=True)
        return exit(2)

    click.echo("Solving FEN")
    click.echo(board)

    click.echo()

    result = get_result(board)

    if result is None:
        click.echo("Unknown result")
    elif result.winner is True:
        click.echo("White wins.")
    elif result.winner is False:
        click.echo("Black wins.")
    else:
        click.echo("Draw.")


if __name__ == "__main__":
    solver()
