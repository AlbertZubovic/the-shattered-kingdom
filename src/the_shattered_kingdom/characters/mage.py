from .character import Character

class Mage(Character):
    """Represent a spellcaster who specializes in powerful magical attacks."""

    def __init__(self, name: str) -> None:
        super().__init__(name, max_hp=80, attack=45, defense=3)


    def introduce(self) -> None:
        """Display the Mage's battlefield introduction."""

        print(f"Arcane energy crackles through the air as {self.name} the Mage emerges from the shadows")
        print("Ancient magic stirs at their fingertips, ready to unleash untold power.", end="\n\n")


    def special_attack(self, target: Character) -> None:
        """Deal 40 damage to the target, ignoring defense."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(f"{self.name} launches a magical fireball.")
        target.take_damage(40 + target.defense)