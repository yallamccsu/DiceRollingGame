# Two-Player Dice Game Engine

A Python-based simulation engine for a two-player dice competition. 
Tracks round-by-round outcomes, win streaks, and roll frequency across 
a full session, then generates a structured post-game report.

## Features

- Simulates any number of rounds between two players
- Tracks wins, losses, and ties across the full session
- Computes each player's longest consecutive win streak
- Records roll frequency and identifies each player's most rolled value
- Full input validation with clean error handling
- Post-game summary report printed automatically at session end

## How to Run

```bash
python Yusuf_Allam_IA7.py
```

You will be prompted to enter the number of rounds. Results are printed 
round by round, followed by a full breakdown at the end.

## Technical Highlights

- `DieVariant` enum makes the die size swappable in one line
- `RoundRecord` dataclass captures the full state of each roll
- `GameReport` auto-computes all stats on initialization
- Isolated RNG via `random.Random` for reproducible results with optional seeding
- Separated rendering logic keeps the engine clean and independently testable

## Tech Stack

Python 3 | dataclasses | enums | functools | collections
