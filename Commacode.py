print("Chethan U, 1AY24AI025, SEC-M")
# Commacode.py

def comma_code(items):
    """
    Given a list of strings, return a single string
    with each item separated by commas, and with
    ', and ' before the last item.
    
    Examples:
      []                 -> ''
      ['apples']         -> 'apples'
      ['apples','bananas'] -> 'apples and bananas'
      ['a','b','c']      -> 'a, b, and c'
    """
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f'{items[0]} and {items[1]}'
    # For 3 or more:
    return ', '.join(items[:-1]) + f', and {items[-1]}'

def main():
    print("Enter your items one per line. Leave blank and press Enter to finish.\n")
    items = []
    while True:
        entry = input(f"Item {len(items)+1}: ").strip()
        if entry == '':
            break
        items.append(entry)

    formatted = comma_code(items)
    if formatted:
        print(f"\nYour list: {formatted}")
    else:
        print("\nYou didn't enter any items!")

if __name__ == '__main__':
    main()
