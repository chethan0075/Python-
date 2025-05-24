print("Chethan U, 1AY24AI025, SEC-M")
# CoinFlipStreaks.py

import random

def simulate_flips(n):
    """Simulate n fair coin flips, returning a list of 'H' or 'T'."""
    return ['H' if random.random() < 0.5 else 'T' for _ in range(n)]

def analyze_streaks(flips):
    """
    Given a list of flips, return:
      - longest head streak
      - longest tail streak
      - dict of streak-length frequencies for heads and tails
    """
    longest = {'H': 0, 'T': 0}
    freqs = {'H': {}, 'T': {}}

    current = flips[0]
    length = 1

    for flip in flips[1:]:
        if flip == current:
            length += 1
        else:
            # record the streak we just ended
            freqs[current][length] = freqs[current].get(length, 0) + 1
            longest[current] = max(longest[current], length)
            # reset for new streak
            current = flip
            length = 1

    # record final streak
    freqs[current][length] = freqs[current].get(length, 0) + 1
    longest[current] = max(longest[current], length)

    return longest, freqs

def main():
    print("Coin Flip Streak Analyzer")
    try:
        n = int(input("How many flips to simulate? "))
        if n <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number; using 100 flips.")
        n = 100

    flips = simulate_flips(n)
    heads = flips.count('H')
    tails = flips.count('T')

    print(f"\nSequence ({n} flips):")
    print(''.join(flips))

    print(f"\nTotal Heads: {heads}, Total Tails: {tails}")

    longest, freqs = analyze_streaks(flips)
    print(f"Longest head streak: {longest['H']}")
    print(f"Longest tail streak: {longest['T']}")

    # Optionally plot histogram of streak lengths
    try:
        import matplotlib.pyplot as plt
        # Build combined histogram data
        all_lengths = []
        labels = []
        for side in ['H','T']:
            for length, count in freqs[side].items():
                all_lengths.extend([length] * count)
                labels.extend([side] * count)
        plt.figure()
        plt.hist([ [l for l, s in zip(all_lengths, labels) if s=='H'],
                   [l for l, s in zip(all_lengths, labels) if s=='T'] ],
                 label=['Heads','Tails'], bins=range(1, max(all_lengths)+2))
        plt.xlabel("Streak Length")
        plt.ylabel("Frequency")
        plt.title("Coin Flip Streak Lengths")
        plt.legend()
        plt.show()
    except ImportError:
        pass  # matplotlib not installed; skip plotting

if __name__ == "__main__":
    main()
