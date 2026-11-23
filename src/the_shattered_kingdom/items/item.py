from abc import ABC, abstractmethod

from the_shattered_kingdom.characters.character import Character


class Item(ABC):
    """Represent an item class with name and description."""

    def __init__(self, name: str, description: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")

        if not name.strip():
            raise ValueError("Item name must not be empty.")


        if not isinstance(description, str):
            raise TypeError("Item description must be a string.")

        if not description.strip():
            raise ValueError("Item description must not be empty.")

        self.__name = name.strip()
        self.__description = description


    @property
    def name(self) -> str:
        return self.__name


    @abstractmethod
    def item_action(self, target: Character) -> None:
        """Describes the characters interaction with the item."""
        pass
