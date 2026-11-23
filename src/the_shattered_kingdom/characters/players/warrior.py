from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.player import Player

class Warrior(Player):
    """Represent a durable melee fighter with a powerful heavy strike."""

    def __init__(self, name: str) -> None:
        super().__init__(name, max_hp=150, attack=30, defense=20)


    def introduce(self) -> None:
        """Display the Warrior's battlefield introduction."""
        print(
            f"Steel clashes as {self.name} the Warrior steps onto the battlefield. "
            "With an unbreakable shield, they stand ready to face any foe.",
            end="\n\n",
        )


    def special_attack(self, target: Character) -> None:
        """Deal 50% more attack damage to the target."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(
            f"{self.name} swings a massive sword with devastating force, "
            f"unleashing a powerful strike against {target.name}!"
        )
        target.take_damage(int(self.attack * 1.5))