from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.inventory import Inventory

class Player(Character):

    def __init__(self, name: str, max_hp: int, attack: int, defense: int) -> None:
        super().__init__(name, max_hp, attack, defense)

        self.__inventory = Inventory()


    @property
    def inventory(self) -> Inventory:
        return self.__inventory