class Character:
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


    def take_damage(self, damage_amount: int) -> bool:
        """Apply damage and return whether the character is still alive."""

        if damage_amount < 1:
            raise ValueError("Damage amount must be greater than 0.")

        if self.__hp > 0:
            self.__hp = max(0, self.__hp - damage_amount)

        if self.__hp == 0:
            print(f"{self.__name} has died.")
            return False

        print(f"{self.__name} takes {damage_amount} damage.")
        return True


    def heal(self, heal_amount: int) -> None:
        """Restore HP up to the maximum, unless the character is dead."""

        if heal_amount < 1:
            raise ValueError("Heal amount must be greater than 0.")

        if self.__hp == 0:
            print(f"{self.__name} has died and cannot be healed.")
        else:
            self.__hp = min(self.__hp + heal_amount, self.__max_hp)

            print(f"{self.__name} heals {heal_amount} HP.")


    def is_alive(self) -> bool:
        """Return whether the character has remaining HP."""

        return self.__hp > 0