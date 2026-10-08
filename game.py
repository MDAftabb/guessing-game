import argparse
import json
import random

from pathlib import Path

SCORES_FILE = Path("scores.json")

DIFFICULTIES = {
    "easy":   {"max": 50,  "tries": 10},
    "medium": {"max": 100, "tries": 7},
    "hard":   {"max": 500, "tries": 9},
}

def load_scores():
    if not SCORES_FILE.exists():
        return
    try:
        with open(SCORES_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return{}

def save_scores(scores):
    with open(SCORES_FILE,"w") as f:
        json.dump(scores,f)


def show_scores(scores):
    """Print the best score for each difficulty."""
    if not scores:
        print("No records yet. Be the first!")
        return
    print("Your best scores:")
    for name, best in scores.items():
        print(f"  {name:<8} {best} attempts")
 
 
def choose_difficulty():
    """Ask until the player picks a valid difficulty."""
    while True:
        choice = input("Choose difficulty (easy/medium/hard): ").lower().strip()
        if choice in DIFFICULTIES:
            return choice
        print("Invalid choice. Try again.")
 
 
def get_guess(high):
    """Keep asking until the player enters a valid whole number in range."""
    while True:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a whole number!")
            continue
 
        if 1 <= guess <= high:
            return guess
        print(f"Pick a number between 1 and {high}.")
 
 
def play_round(difficulty):
    """Play one game. Return the attempts if won, else None."""
    max_number = DIFFICULTIES[difficulty]["max"]
    max_tries = DIFFICULTIES[difficulty]["tries"]
 
    secret = random.randint(1, max_number)
    attempts = 0
    previous_distance = None
 
    print(f"\nI'm thinking of a number between 1 and {max_number}.")
    print(f"You have {max_tries} tries.")
 
    while attempts < max_tries:
        guess = get_guess(max_number)
        attempts += 1
 
        if guess == secret:
            print(f"Correct! You got it in {attempts} attempts.")
            return attempts
 
        print("Too low!" if guess < secret else "Too high!")
 
        # Warmer / colder hint
        distance = abs(guess - secret)
        if previous_distance is not None:
            if distance < previous_distance:
                print("Warmer!")
            elif distance > previous_distance:
                print("Colder!")
            else:
                print("Same distance as before.")
        previous_distance = distance
 
        # Even/odd hint after 3 wrong guesses
        if attempts == 3:
            parity = "even" if secret % 2 == 0 else "odd"
            print(f"Hint: the number is {parity}.")
 
        print(f"Tries left: {max_tries - attempts}")
 
    print(f"Out of tries! The number was {secret}.")
    return None
 
 
def update_score(scores, difficulty, attempts):
    """Save a new record if the player beat their best."""
    best = scores.get(difficulty)
    if best is None or attempts < best:
        scores[difficulty] = attempts
        save_scores(scores)
        print("New record!")
    else:
        print(f"Your best on {difficulty} is {best} attempts.")
 
 
def main():
    parser = argparse.ArgumentParser(description="Number guessing game")
    parser.add_argument("--difficulty", choices=DIFFICULTIES,
                        help="skip the menu and use this difficulty")
    args = parser.parse_args()
 
    scores = load_scores()
 
    print("=== Number Guessing Game ===")
    show_scores(scores)
    print()
 
    while True:
        difficulty = args.difficulty or choose_difficulty()
        attempts = play_round(difficulty)
 
        if attempts is not None:
            update_score(scores, difficulty, attempts)
 
        again = input("Play again? (y/n): ").lower().strip()
        if again != "y":
            break
 
    print("Thanks for playing!")

if __name__=="__main__":
    main()
