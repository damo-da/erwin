import click

from .two_knights import two_knights


@click.group
def solve():
    """Solve endgame positions."""


# noinspection PyTypeChecker
solve.add_command(two_knights)
