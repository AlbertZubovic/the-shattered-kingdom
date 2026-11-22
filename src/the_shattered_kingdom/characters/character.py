from abc import ABC, abstractmethod

class Character(ABC):
    """Represent a class with combat statistics and health."""

    def __init__(self, name: str, max_hp: int, attack: int, defense: int) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        if not name.strip():
            raise ValueError("Name must not be empty.")

        if type(max_hp) is not int:
            raise TypeError("Max HP must be an int.")

        if max_hp <= 0:
            raise ValueError("Max HP must be greater than 0.")

        if type(attack) is not int:
            raise TypeError("Attack must be an int.")

        if attack < 0:
            raise ValueError("Attack must be greater than or equal to 0.")

        if type(defense) is not int:
            raise TypeError("Defense must be an int.")

        if defense < 0:
            raise ValueError("Defense must be greater than or equal to 0.")

        self.__name = name.strip()
        self.__max_hp = max_hp
        self.__hp = max_hp
        self.__attack = attack
        self.__defense = defense


    @abstractmethod
    def introduce(self) -> None:
        """Display the Characters's battlefield introduction."""

        pass


    @property
    def name(self) -> str:
        return self.__name

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def attack(self) -> int:
        return self.__attack

    @ property
    def defense(self) -> int:
        return self.__defense


    def __str__(self) -> str:
        return f"Hero: {self.__name} | HP: {self.__hp}/{self.__max_hp} | ATK: {self.__attack} | DEF: {self.__defense}"


    def take_damage(self, damage_amount: int) -> int:
        """Apply damage after defense and return the actual HP lost."""

        if damage_amount < 1:
            raise ValueError("Damage amount must be greater than 0.")

        if not self.is_alive():
            return 0

        damage_taken = min(self.__hp, max(1, damage_amount - self.__defense))

        print(f"{self.__name} takes {damage_taken} damage.")

        self.__hp -= damage_taken

        if self.__hp == 0:
            print(f"{self.__name} has died.")

        print(f"{self.__name} has {self.__hp} HP remaining.")

        return damage_taken


    def heal(self, heal_amount: int) -> int:
        """Restore HP up to the maximum, unless the character is dead."""

        if heal_amount < 1:
            raise ValueError("Heal amount must be greater than 0.")

        if self.__hp == 0:
            print(f"{self.__name} has died and cannot be healed.")
            return 0
        else:
            total_heal = min(heal_amount, self.__max_hp - self.__hp)
            self.__hp += total_heal

            print(f"{self.__name} heals {total_heal} HP.")
            return total_heal


    def is_alive(self) -> bool:
        """Return whether the character has remaining HP."""

        return self.__hp > 0

    def attack_target(self, target: Character) -> None:
        """Deals damage to a target Character."""
        if not isinstance(target, Character):
            raise TypeError(f"The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        target.take_damage(max(1, self.__attack))