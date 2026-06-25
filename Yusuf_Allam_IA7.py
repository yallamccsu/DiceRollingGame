import random
import math
import sys
from typing import List, Dict, Tuple, Optional
from functools import reduce
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import Counter


class DieVariant(Enum):
    D6  = 6
    D8  = 8
    D10 = 10
    D12 = 12
    D20 = 20


ACTIVE_DIE = DieVariant.D6

FONT_DEFAULT = ('Arial', 11)


def _validate_round_count(raw: str) -> int:
    try:
        val = int(raw)
        if val <= 0 or math.isinf(val):
            raise ValueError
        return val
    except (ValueError, TypeError):
        raise ValueError(f"invalid round count: {raw!r}")


def _roll(variant: DieVariant, rng: random.Random) -> int:
    return rng.randint(1, variant.value)


def _evaluate_roll(r1: int, r2: int) -> int:
    # returns 1 if player 1 wins, 2 if player 2 wins, 0 for tie
    if r1 == r2:
        return 0
    return 1 if r1 > r2 else 2


def _build_frequency_map(rolls: List[int]) -> Dict[int, int]:
    return dict(Counter(rolls))


def _compute_streak(results: List[int], player: int) -> int:
    # longest consecutive win streak for a given player
    best = 0
    curr = 0
    for r in results:
        if r == player:
            curr += 1
            best = max(best, curr)
        else:
            curr = 0
    return best


@dataclass
class RoundRecord:
    round_number: int
    roll_p1: int
    roll_p2: int
    winner: int

    def summary(self) -> str:
        result = (
            "tie" if self.winner == 0
            else f"player {self.winner} wins"
        )
        return f"round {self.round_number}: player 1 rolls {self.roll_p1}, player 2 rolls {self.roll_p2} | {result}"


@dataclass
class GameReport:
    records: List[RoundRecord]
    die: DieVariant
    wins: Dict[int, int]       = field(init=False)
    ties: int                  = field(init=False)
    streaks: Dict[int, int]    = field(init=False)
    roll_freq: Dict[int, Dict[int, int]] = field(init=False)
    overall_winner: str        = field(init=False)

    def __post_init__(self):
        outcome_seq = [r.winner for r in self.records]
        self.wins = {
            1: outcome_seq.count(1),
            2: outcome_seq.count(2),
        }
        self.ties = outcome_seq.count(0)
        self.streaks = {
            1: _compute_streak(outcome_seq, 1),
            2: _compute_streak(outcome_seq, 2),
        }
        self.roll_freq = {
            1: _build_frequency_map([r.roll_p1 for r in self.records]),
            2: _build_frequency_map([r.roll_p2 for r in self.records]),
        }
        self.overall_winner = self._resolve_winner()

    def _resolve_winner(self) -> str:
        if self.wins[1] == self.wins[2]:
            return "tie"
        return f"player {1 if self.wins[1] > self.wins[2] else 2}"


class DiceEngine:
    def __init__(self, die: DieVariant = ACTIVE_DIE, seed: Optional[int] = None):
        self.die = die
        self._rng = random.Random(seed)
        self._records: List[RoundRecord] = []

    def play_round(self, round_number: int) -> RoundRecord:
        r1 = _roll(self.die, self._rng)
        r2 = _roll(self.die, self._rng)
        winner = _evaluate_roll(r1, r2)
        record = RoundRecord(round_number, r1, r2, winner)
        self._records.append(record)
        return record

    def run_game(self, rounds: int) -> GameReport:
        for i in range(1, rounds + 1):
            self.play_round(i)
        return GameReport(records=list(self._records), die=self.die)

    def clear(self):
        self._records.clear()


class GameRenderer:
    @staticmethod
    def render(report: GameReport):
        print(f"\ndice game | {report.die.name}\n")

        for record in report.records:
            print(f"  {record.summary()}")

        print(f"\n  {'final score':}")
        print(f"  {'-' * 30}")
        for p in [1, 2]:
            print(f"  player {p} wins  : {report.wins[p]}")
        print(f"  ties        : {report.ties}")

        print(f"\n  longest streaks")
        for p in [1, 2]:
            print(f"  player {p}       : {report.streaks[p]}")

        print(f"\n  most rolled")
        for p in [1, 2]:
            freq = report.roll_freq[p]
            if freq:
                top = max(freq, key=lambda k: freq[k])
                print(f"  player {p}       : {top} ({freq[top]}x)")

        print(f"\n  overall winner: {report.overall_winner}\n")


def main():
    try:
        raw = input("how many rounds? ")
        rounds = _validate_round_count(raw)
    except ValueError as e:
        print(f"error: {e}")
        sys.exit(1)

    engine = DiceEngine()
    report = engine.run_game(rounds)
    GameRenderer.render(report)


if __name__ == "__main__":
    main()
