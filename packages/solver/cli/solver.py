import click

from solver.algo import Resolver
from .options import OPTION_FEN


@click.command()
@click.option("--fen", **OPTION_FEN)
def solver(fen: str, variant: str = "antichess"):
    """Solve a given FEN."""

    click.echo("Solving FEN")

    # board: Board
    # if variant == "antichess":
    #     board = AntichessBoard(fen)
    # else:
    #     click.echo(f"Unknown variant: {variant}.", err=True)
    #     return exit(2)

    # click.echo(board)

    click.echo()

    result = Resolver().get_result(starting_fen=fen)

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
