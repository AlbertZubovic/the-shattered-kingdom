from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.player import Player

class Rogue(Player):
    """Represent an agile fighter capable of striking twice in succession."""

    def __init__(self, name: str) -> None:
        super().__init__(name, max_hp=100, attack=35, defense=7)


    def introduce(self) -> None:
        """Display the Rogue's battlefield introduction."""
        print(
            f"From the darkness steps {self.name} the Rogue, blades gleaming beneath a shadowed cloak. "
            "Swift, silent, and deadly, they strike before their enemies even sense danger.",
            end="\n\n",
        )


    def special_attack(self, target: Character) -> None:
        """Strike the target twice in quick succession."""

        if not isinstance(target, Character):
            raise TypeError("The target is not a Character.")

        if not self.is_alive():
            raise ValueError("Dead characters cannot attack.")

        print(
            f"{self.name} lunges forward, slashing {target.name} with a swift dagger strike!"
        )
        target.take_damage(self.attack)

        print(
            f"Before {target.name} can react, {self.name} strikes again "
            "with a second dagger attack, catching them completely off guard!"
        )
        target.take_damage(self.attack)
