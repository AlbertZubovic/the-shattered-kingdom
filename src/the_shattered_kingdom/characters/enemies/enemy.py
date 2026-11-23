from abc import abstractmethod

from the_shattered_kingdom.characters.character import Character

class Enemy(Character):
    """Represent an enemy that defines its own combat behavior."""

    @abstractmethod
    def choose_action(self, target: Character) -> None:
        """Select and execute an attack against the target."""

        pass