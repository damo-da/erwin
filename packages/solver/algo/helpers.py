from typing import Optional

from chess import Outcome, Termination

WIN = Termination.VARIANT_WIN
DRAW = Termination.VARIANT_DRAW
LOSS = Termination.VARIANT_LOSS

MAX_DEPTH = 6


def fix_outcome(o: Optional[Outcome]) -> Optional[Outcome]:
    if o is None: return None

    if o.termination == LOSS:
        o.termination = WIN
        o.winner = not o.winner

    elif o.termination in (Termination.INSUFFICIENT_MATERIAL, Termination.THREEFOLD_REPETITION):
        o.termination = DRAW

    if o.termination not in (WIN, DRAW):
        raise Exception("Unknown outcome", o)

    return o
