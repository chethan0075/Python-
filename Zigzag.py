print("Chethan U, 1AY24AI025, SEC-M")
# Zigzag.py

def convert_zigzag(s: str, num_rows: int) -> str:
    if num_rows == 1 or num_rows >= len(s):
        return s

    # Create a list for each row
    rows = [''] * num_rows
    cur_row = 0
    going_down = False

    # Build the zigzag row by row
    for char in s:
        rows[cur_row] += char
        # Change direction at top/bottom
        if cur_row == 0 or cur_row == num_rows - 1:
            going_down = not going_down
        cur_row += 1 if going_down else -1

    # Combine rows
    return ''.join(rows)

def print_zigzag_pattern(s: str, num_rows: int) -> None:
    if num_rows == 1:
        print(s)
        return

    # Build a 2D grid filled with spaces
    # Estimate width: roughly len(s) // (num_rows - 1) * (num_rows - 1)
    width = len(s)
    grid = [[' ' for _ in range(width)] for _ in range(num_rows)]

    row, col = 0, 0
    going_down = True

    for char in s:
        grid[row][col] = char
        if row == 0:
            going_down = True
        elif row == num_rows - 1:
            going_down = False

        if going_down:
            row += 1
        else:
            row -= 1
            col += 1

    # Print each row
    for r in grid:
        print(''.join(r).rstrip())

def main():
    print("Zigzag Conversion")
    s = input("Enter the string to convert: ")
    try:
        num_rows = int(input("Enter number of rows: "))
    except ValueError:
        print("Invalid number of rows. Using 1.")
        num_rows = 1

    print("\nZigzag pattern:")
    print_zigzag_pattern(s, num_rows)

    result = convert_zigzag(s, num_rows)
    print(f"\nConverted output: {result}")

if __name__ == "__main__":
    main()
