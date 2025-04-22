import random


# Simulates rolling a six-sided die
def roll_dice():
    """Returns a random number between 1 and 6."""
    return random.randint(1, 6)


# Determines the winner of a single round and prints the result
def play_round(player1_roll, player2_roll):
    """
    Compares two dice rolls and returns the round result.

    Args:
    player1_roll (int): Dice roll for Player 1.
    player2_roll (int): Dice roll for Player 2.

    Returns:
    str: "Player 1", "Player 2", or "Tie"
    """
    if player1_roll > player2_roll:
        print(f"Player 1 rolls a {player1_roll}, Player 2 rolls a {player2_roll}. Player 1 wins the round.")
        return "Player 1"
    elif player2_roll > player1_roll:
        print(f"Player 1 rolls a {player1_roll}, Player 2 rolls a {player2_roll}. Player 2 wins the round.")
        return "Player 2"
    else:
        print(f"Player 1 rolls a {player1_roll}, Player 2 rolls a {player2_roll}. The round is a tie.")
        return "Tie"


# Runs the full game: handles input, rounds, scoring, and final result
def main():
    player1_score = 0
    player2_score = 0
    tie_score = 0

    # Prompt user for number of rounds
    rounds = int(input("How many rounds do you want to play? "))

    # Play each round and update scores
    for _ in range(rounds):
        player1_roll = roll_dice()
        player2_roll = roll_dice()
        result = play_round(player1_roll, player2_roll)

        if result == "Player 1":
            player1_score += 1
        elif result == "Player 2":
            player2_score += 1
        else:
            tie_score += 1

    # Display final results
    print(f"\nFinal Score: Player 1 wins {player1_score} round(s). "
          f"Player 2 wins {player2_score} round(s). {tie_score} round(s) ended in a tie.")

    # Announce overall winner
    if player1_score > player2_score:
        print("Overall Winner: Player 1!")
    elif player2_score > player1_score:
        print("Overall Winner: Player 2!")
    else:
        print("The game ends in a tie!")


# Execute the game
if __name__ == "__main__":
    main()
