from the_shattered_kingdom.items.item import Item

class Inventory():
    """Represent a character inventory with a dictionary of items."""

    def __init__(self):
        self.__items : dict[Item: int] = dict()


    def add_item(self, item: Item, amount: int = 1) -> None:
        """Adds a valid item to the invenotry."""

        if not isinstance(item, Item):
            raise TypeError("Item is not a valid item.")

        if type(amount) is not int or amount < 1:
            raise ValueError("Amount must be a positive integer.")

        self.__items[item] = self.__items.get(item, 0) + amount


    def remove_item(self, item: Item, amount: int = 1) -> None:
        """Remove a valid item from the inventory."""

        if not isinstance(item, Item):
            raise TypeError("Item is not a valid item.")

        if type(amount) is not int or amount < 1:
            raise ValueError("Amount must be a positive integer.")

        if self.__items.get(item, 0) < amount:
            raise ValueError("Item does not exist or insufficient quantity.")

        self.__items[item] -= amount

        if self.__items[item] == 0:
            del self.__items[item]


    def clear_inventory(self):
        """Clears all items in the inventory."""

        self.__items.clear()


    def list_items(self) -> None:
        """Lists all items in the inventory and their amounts."""
        if not self.__items:
            print("Inventory is empty.")
            return

        print("\n===== INVENTORY =====")
        print(f"{'Item':<20} {'Quantity':>10}")
        print("-" * 31)

        for item, amount in self.__items.items():
            print(f"{item.name:<20} {amount:>10}")

        print("=" * 31)