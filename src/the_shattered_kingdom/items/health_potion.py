from the_shattered_kingdom.items.item import Item

from the_shattered_kingdom.characters.character import Character


class HealthPotion(Item):
    """Represents the Health Potion class that heals players."""

    def __init__(self, name: str, description: str, heal_amount: int) -> None:
        super().__init__(name, description)

        if type(heal_amount) is not int:
            raise TypeError("Heal amount must be a number.")

        if heal_amount < 1:
            raise ValueError("Heal amount must be greater than 0.")

        self.__heal_amount = heal_amount


    def item_action(self, target: Character) -> None:
        """Heals the player with the heal amount."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        heal_amount = target.heal(self.__heal_amount)
        print(f"{target.name} has applied a heal potion and has healed {heal_amount}.")