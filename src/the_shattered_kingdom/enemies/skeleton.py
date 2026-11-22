from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.enemies.enemy import Enemy

class Skeleton(Enemy):
    """Represent a skeleton that drains life every second turn."""

    def __init__(self, name):
        super().__init__(name, max_hp=95, attack=25, defense=12)

        self.__xp_reward = 25
        self.__turn_counter = 0


    def introduce(self) -> None:
        """Introduce the Skeleton."""
        print(
            f"The ground trembles as {self.name}, the Skeleton, rises from the grave! "
            "With hollow eyes and a blade worn by centuries, "
            "this restless warrior prepares for battle once more!",
            end="\n\n"
        )


    def choose_action(self, target: Character) -> None:
        """Use Life Drain every second turn; otherwise attack normally."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        self.__turn_counter += 1

        if not self.__turn_counter % 2:
            self.special_attack(target)
        else:
            self.attack_target(target)


    def special_attack(self, target: Character) -> None:
        """Deal damage after defense and heal for half the actual damage dealt."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(
            f"{self.name} the Skeleton raises its cursed blade and strikes {target.name}, "
            "draining their life force with dark necromantic magic!"
        )

        total_damage = target.take_damage(self.attack)
        heal_amount = total_damage // 2

        total_heal = self.heal(heal_amount) if heal_amount > 0 else 0

        print(
            f"Dark energy flows back into {self.name}, "
            f"restoring {total_heal} HP from the stolen life force!"
        )