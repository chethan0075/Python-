print("Chethan U, 1AY24AI025, SEC-M")
#!/usr/bin/env python3
# FantasyGameInventory.py

import json
import sys

class Item:
    def __init__(self, name: str, weight: float, max_stack: int = 1):
        self.name = name
        self.weight = weight
        self.max_stack = max_stack

    def __repr__(self):
        return f"{self.name}(wt:{self.weight}, max_stack:{self.max_stack})"


class Inventory:
    def __init__(self, max_slots: int = 20, max_weight: float = 100.0):
        self.max_slots = max_slots
        self.max_weight = max_weight
        # stored as dict name -> [Item prototype, quantity]
        self.contents: dict[str, list] = {}

    def total_weight(self) -> float:
        return sum(item.weight * qty for item, qty in self.contents.values())

    def used_slots(self) -> int:
        # each stack occupies one slot
        return len(self.contents)

    def can_add(self, item: Item, qty: int) -> bool:
        new_weight = self.total_weight() + item.weight * qty
        if new_weight > self.max_weight:
            print(f"❌ Cannot add: would exceed weight ({new_weight:.1f}/{self.max_weight})")
            return False
        if item.name in self.contents:
            current_qty = self.contents[item.name][1]
            # same slot, but check stack limit
            if current_qty + qty > item.max_stack:
                print(f"❌ Cannot add: would exceed stack limit ({current_qty + qty}/{item.max_stack})")
                return False
            return True
        else:
            # new slot needed
            if self.used_slots() + 1 > self.max_slots:
                print(f"❌ Cannot add: no free slots ({self.used_slots()}/{self.max_slots})")
                return False
            if qty > item.max_stack:
                print(f"❌ Cannot add: exceeds single-stack size ({qty}/{item.max_stack})")
                return False
            return True

    def add_item(self, item: Item, qty: int = 1) -> bool:
        if not self.can_add(item, qty):
            return False
        if item.name in self.contents:
            self.contents[item.name][1] += qty
        else:
            self.contents[item.name] = [item, qty]
        print(f"✅ Added {qty}× {item.name}.")
        return True

    def remove_item(self, name: str, qty: int = 1) -> bool:
        if name not in self.contents:
            print(f"❌ No {name} in inventory.")
            return False
        item, current_qty = self.contents[name]
        if qty > current_qty:
            print(f"❌ You only have {current_qty}× {name}.")
            return False
        if qty == current_qty:
            del self.contents[name]
        else:
            self.contents[name][1] -= qty
        print(f"✅ Removed {qty}× {name}.")
        return True

    def list_items(self):
        if not self.contents:
            print("(empty)")
            return
        print(f"\nInventory ({self.used_slots()}/{self.max_slots} slots, "
              f"{self.total_weight():.1f}/{self.max_weight} wt):")
        for item, qty in self.contents.values():
            print(f"  - {item.name}: {qty}×  (wt each {item.weight}, total {item.weight*qty:.1f})")
        print()

    def save(self, path: str):
        data = {
            "max_slots": self.max_slots,
            "max_weight": self.max_weight,
            "contents": [
                {"name": item.name, "weight": item.weight,
                 "max_stack": item.max_stack, "qty": qty}
                for item, qty in self.contents.values()
            ]
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Inventory saved to {path}")

    def load(self, path: str):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load {path}: {e}")
            return
        self.max_slots = data.get("max_slots", self.max_slots)
        self.max_weight = data.get("max_weight", self.max_weight)
        self.contents.clear()
        for entry in data.get("contents", []):
            item = Item(entry["name"], entry["weight"], entry["max_stack"])
            self.contents[item.name] = [item, entry["qty"]]
        print(f"✅ Inventory loaded from {path}")


def main():
    inv = Inventory(max_slots=15, max_weight=75.0)
    # Example shop catalog
    catalog = {
        "Health Potion": Item("Health Potion", weight=0.5, max_stack=10),
        "Mana Potion":   Item("Mana Potion",   weight=0.4, max_stack=10),
        "Iron Sword":    Item("Iron Sword",    weight=5.0, max_stack=1),
        "Arrow":         Item("Arrow",         weight=0.1, max_stack=50),
        "Shield":        Item("Shield",        weight=7.0, max_stack=1),
    }

    MENU = """
Choose an action:
  1) List inventory
  2) Add item
  3) Remove item
  4) Save inventory
  5) Load inventory
  6) Exit
> """

    while True:
        choice = input(MENU).strip()
        if choice == '1':
            inv.list_items()
        elif choice == '2':
            print("Available items to add:")
            for idx, name in enumerate(catalog, 1):
                it = catalog[name]
                print(f"  {idx}) {name} (wt {it.weight}, stack {it.max_stack})")
            sel = input("Select item number: ").strip()
            qty = input("Quantity: ").strip()
            try:
                sel_i = int(sel) - 1
                qty_i = int(qty)
                name = list(catalog.keys())[sel_i]
                inv.add_item(catalog[name], qty_i)
            except Exception:
                print("❌ Invalid selection or quantity.")
        elif choice == '3':
            name = input("Enter item name to remove: ").strip()
            qty = input("Quantity to remove: ").strip()
            try:
                qty_i = int(qty)
                inv.remove_item(name, qty_i)
            except ValueError:
                print("❌ Invalid quantity.")
        elif choice == '4':
            path = input("Save file path: ").strip()
            inv.save(path)
        elif choice == '5':
            path = input("Load file path: ").strip()
            inv.load(path)
        elif choice == '6':
            print("Goodbye, adventurer!")
            sys.exit(0)
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
