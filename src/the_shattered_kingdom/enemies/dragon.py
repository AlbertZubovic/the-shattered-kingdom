from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.enemies.enemy import Enemy

class Dragon(Enemy):
    """Represent a dragon that unleashes an inferno every fourth turn."""

    def __init__(self, name):
        super().__init__(name, max_hp=220, attack=40, defense=18)

        self.__xp_reward = 150
        self.__turn_counter = 0


    def introduce(self) -> None:
        """Introduce the Dragon."""

        print(
            f"The skies darken as {self.name}, the Dragon, descends upon the battlefield! "
            "Flames dance between its razor-sharp teeth, "
            "and its thunderous roar shakes the very foundations of the kingdom!",
            end="\n\n"
        )


    def choose_action(self, target: Character) -> None:
        """Use Inferno every fourth turn; otherwise attack normally."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        self.__turn_counter += 1

        if not self.__turn_counter % 4:
            self.special_attack(target)
        else:
            self.attack_target(target)


    def special_attack(self, target: Character) -> None:
        """Unleash Inferno to deal 50 damage ignoring defense."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(
            f"{self.name} the Dragon unleashes a deafening roar before engulfing {target.name} "
            "in a raging inferno of scorching flames, burning through even the strongest armor!"
        )

        target.take_damage(50 + target.defense)
