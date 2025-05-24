print("Chethan U, 1AY24AI025, SEC-M")
# Collatzsequence.py

def collatz_sequence(n):
    """
    Generate the Collatz sequence starting from n.
    Yields each term of the sequence, including the starting n and ending 1.
    """
    while True:
        yield n
        if n == 1:
            break
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

def main():
    print("Collatz Sequence Generator")
    try:
        start = int(input("Enter a positive integer to start the sequence: "))
        if start <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        return

    seq = list(collatz_sequence(start))
    print("\nCollatz sequence:")
    print(" → ".join(map(str, seq)))

    steps = len(seq) - 1
    print(f"\nTotal steps to reach 1: {steps}")

if __name__ == "__main__":
    main()
