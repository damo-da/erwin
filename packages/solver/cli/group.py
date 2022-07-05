import click

from .endgame import solve as endgame
from .fen import solver as fen_solver


@click.group
def cli() -> None:
    """Erwin the chess engine."""


# noinspection PyTypeChecker
cli.add_command(endgame, name="endgame")
# noinspection PyTypeChecker
cli.add_command(fen_solver, name="fen")
