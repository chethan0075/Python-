print("Chethan U, 1AY24AI025, SEC-M")
#!/usr/bin/env python3
# ChessDictionaryValidator.py

import sys
import json
import re

# Allowed piece codes and maximum counts per side
MAX_COUNTS = {
    'K': 1,  # King
    'Q': 1,  # Queen (you could allow promotions, but we cap at 1 here)
    'R': 2,  # Rooks
    'B': 2,  # Bishops
    'N': 2,  # Knights
    'P': 8,  # Pawns
}

FILE_ERROR = """
Usage:
  python ChessDictionaryValidator.py path/to/position.json
Where the JSON should be an object like:
  {{
    "e4": "wP",
    "e5": "bP",
    "g1": "wN",
    …
  }}
"""

def load_position(path):
    """Load the JSON file and ensure it’s a dict."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading '{path}': {e}")
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"Error: JSON root must be an object mapping squares to pieces.")
        sys.exit(1)
    return data

def validate_squares(position):
    """Ensure every key is a valid square a1–h8, no duplicates."""
    square_pattern = re.compile(r'^[a-h][1-8]$')
    invalid = [sq for sq in position if not square_pattern.match(sq)]
    if invalid:
        print("Invalid square names:", ", ".join(invalid))
        return False
    return True

def validate_pieces(position):
    """
    Ensure every value is a valid piece code: 
    wK, wQ, wR, wB, wN, wP or bK, …, bP.
    Also count pieces per side.
    """
    piece_pattern = re.compile(r'^[wb][KQRBNP]$')
    counts = {
        'w': {k: 0 for k in MAX_COUNTS},
        'b': {k: 0 for k in MAX_COUNTS},
    }
    bad = []
    for sq, piece in position.items():
        if not piece_pattern.match(piece):
            bad.append(f"{sq}: '{piece}'")
        else:
            side, p = piece[0], piece[1]
            counts[side][p] += 1

    if bad:
        print("Invalid piece codes:")
        for entry in bad:
            print(" ", entry)
        return False

    ok = True
    # Check maximums and required kings
    for side in ['w', 'b']:
        # king exactly 1
        k = counts[side]['K']
        if k != 1:
            print(f"Side '{side}' has {k} kings (must be exactly 1).")
            ok = False
        # other pieces ≤ max
        for p, mx in MAX_COUNTS.items():
            if counts[side][p] > mx:
                print(f"Side '{side}' has {counts[side][p]} '{p}'s (max {mx}).")
                ok = False
    return ok

def main():
    if len(sys.argv) != 2:
        print(FILE_ERROR)
        sys.exit(1)

    path = sys.argv[1]
    position = load_position(path)

    print(f"Loaded position with {len(position)} occupied squares.")
    sq_ok = validate_squares(position)
    pc_ok = validate_pieces(position)

    if sq_ok and pc_ok:
        print("✅ Position is valid.")
        sys.exit(0)
    else:
        print("❌ Position is INVALID.")
        sys.exit(2)

if __name__ == "__main__":
    main()
