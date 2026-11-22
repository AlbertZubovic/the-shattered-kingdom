from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.enemies.enemy import Enemy

class Goblin(Enemy):
    """Represent a goblin that uses a dirty trick every third turn."""

    def __init__(self, name):
        super().__init__(name, max_hp=60, attack=18, defense=5)

        self.__xp_reward = 10
        self.__turn_counter = 0


    def introduce(self) -> None:
        """Introduce the Goblin."""

        print(
            f"From the shadows scurries {self.name}, the Goblin! "
            "With a wicked grin and a rusted dagger, "
            "this cunning creature is ready to cause chaos!",
            end="\n\n"
        )


    def choose_action(self, target: Character) -> None:
        """Perform a dirty trick every third turn; otherwise attack normally."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        self.__turn_counter += 1

        if not self.__turn_counter % 3:
            self.special_attack(target)
        else:
            self.attack_target(target)


    def special_attack(self, target: Character) -> None:
        """Ignore defense to deal 10 damage and restore 5 HP."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(
            f"{self.name} the Goblin throws dirt into {target.name}'s eyes "
            "and lands a sneaky dagger strike!"
        )
        target.take_damage(10 + target.defense)
        total_heal = self.heal(5)

        print(f"{self.name} the Goblin steals {total_heal} HP worth of vitality!")

