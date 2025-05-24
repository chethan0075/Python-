print("Chethan U, 1AY24AI025, SEC-M")
#!/usr/bin/env python3
# ZombieDiceBots.py

import random
from collections import Counter, deque

# --- Game constants ---

# Dice colors and their face distributions:
#   Green dice   (6): 3 Brains, 2 Footsteps, 1 Shotgun
#   Yellow dice  (4): 2 Brains, 2 Footsteps, 2 Shotgun
#   Red dice     (3): 1 Brain, 2 Footsteps, 3 Shotgun
DICE_POOL = ['G'] * 6 + ['Y'] * 4 + ['R'] * 3
FACES = {
    'G': ['B','B','B','F','F','S'],
    'Y': ['B','B','F','F','S','S'],
    'R': ['B','F','F','S','S','S'],
}

# Win condition
TARGET_BRAINS = 13

# --- Bot strategy functions ---

def cautious_bot(state):
    """
    Stop as soon as you've collected >= 2 brains this turn.
    """
    return state['brains_this_turn'] < 2

def risky_bot(state):
    """
    Keep rolling until you get at least 1 shotgun this turn.
    """
    return state['shotguns_this_turn'] == 0

def random_bot(state):
    """
    Flip a coin each decision to keep rolling or stop.
    """
    return random.choice([True, False])

def always_push_bot(state):
    """
    Never stop until you die (3 shotguns) or cup empties.
    """
    return True

# You can add more strategies here!

# --- Core game simulation ---

class ZombieDiceGame:
    def __init__(self, players):
        """
        players: list of tuples (name, strategy_function)
        """
        self.players = players
        self.scores = {name: 0 for name, _ in players}
        self.turn_order = deque(name for name, _ in players)

    def draw_dice(self, cup, num=3):
        """
        Draw up to `num` dice from the cup at random.
        """
        draw = []
        for _ in range(min(num, len(cup))):
            die = random.choice(cup)
            cup.remove(die)
            draw.append(die)
        return draw

    def play_turn(self, name, strategy_fn):
        """
        Play a single turn for `name`, using `strategy_fn` to decide
        whether to continue rolling. Update `self.scores[name]` when done.
        Returns True if won this turn.
        """
        # Set up fresh cup and "footsteps" rack
        cup = DICE_POOL.copy()
        footprints = []
        brains_collected = 0
        shotguns_collected = 0

        # State passed to bot
        state = {
            'total_score': self.scores[name],
            'brains_this_turn': 0,
            'shotguns_this_turn': 0
        }

        while True:
            # Refill your hand to 3 dice, preferring footprints from last roll
            hand = footprints + self.draw_dice(cup, 3 - len(footprints))
            footprints = []

            if not hand:
                break  # no dice left

            # Roll each die in hand
            for die in hand:
                face = random.choice(FACES[die])
                if face == 'B':
                    brains_collected += 1
                elif face == 'S':
                    shotguns_collected += 1
                else:  # 'F'
                    footprints.append(die)

            # Update state for strategy decision
            state['brains_this_turn'] = brains_collected
            state['shotguns_this_turn'] = shotguns_collected

            # If eaten (3 shotguns), turn ends, no brains score
            if shotguns_collected >= 3:
                print(f"  {name} got 3 shotguns and busts (0 this turn).")
                return False

            # Ask bot whether to continue
            if not strategy_fn(state):
                # bank brains and end turn
                self.scores[name] += brains_collected
                print(f"  {name} stops with +{brains_collected} brains (total {self.scores[name]}).")
                return self.scores[name] >= TARGET_BRAINS

        # cup emptied: bank brains
        self.scores[name] += brains_collected
        print(f"  {name} ran out of dice, banks +{brains_collected} brains (total {self.scores[name]}).")
        return self.scores[name] >= TARGET_BRAINS

    def play_round(self):
        """
        Play one full round (each player one turn).
        Return the winner's name or None if none reached target.
        """
        for name, strat in self.players:
            print(f"{name}'s turn (score={self.scores[name]})...")
            won = self.play_turn(name, strat)
            if won:
                return name
        return None

    def run_game(self, verbose=True):
        """
        Play rounds until a player reaches TARGET_BRAINS.
        Returns winner name.
        """
        if verbose:
            print(f"=== Starting game to {TARGET_BRAINS} brains ===")
        while True:
            winner = self.play_round()
            if winner:
                if verbose:
                    print(f"🎉 {winner} wins with {self.scores[winner]} brains! 🎉")
                return winner

# --- Tournament manager ---

def run_tournament(bots, num_games=1000):
    """
    bots: list of (name, strategy_fn)
    Returns win counts per bot after `num_games` plays.
    """
    wins = Counter()
    for i in range(1, num_games+1):
        game = ZombieDiceGame(bots)
        winner = game.run_game(verbose=False)
        wins[winner] += 1
        if i % (num_games//10) == 0:
            print(f"  Completed {i}/{num_games} games...")
    return wins

# --- Main entrypoint ---

def main():
    # Define which bots participate
    bots = [
        ("Cautious", cautious_bot),
        ("Risky",    risky_bot),
        ("Random",   random_bot),
        ("AllIn",    always_push_bot),
    ]
    print("Zombie Dice Bots Simulation")
    mode = input("Enter [1] single game, [2] tournament: ").strip()
    if mode == '1':
        game = ZombieDiceGame(bots)
        game.run_game()
    elif mode == '2':
        try:
            n = int(input("Number of games to simulate (e.g. 1000): "))
        except ValueError:
            n = 1000
        results = run_tournament(bots, num_games=n)
        print("\nTournament results:")
        for name,_ in bots:
            print(f"  {name}: {results[name]} wins ({results[name]*100/n:.1f}%)")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
