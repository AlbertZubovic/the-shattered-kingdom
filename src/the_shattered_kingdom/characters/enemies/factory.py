from the_shattered_kingdom.characters.enemies.enemy import Enemy

from the_shattered_kingdom.characters.enemies.dragon import Dragon
from the_shattered_kingdom.characters.enemies.goblin import Goblin
from the_shattered_kingdom.characters.enemies.skeleton import Skeleton

ENEMY_CLASSES = {
    "dragon": Dragon,
    "goblin": Goblin,
    "skeleton": Skeleton,
}


def create_enemy(name: str, enemy_type: str) -> Enemy:
    """Create an enemy of the requested type."""

    if not isinstance(enemy_type, str):
        raise TypeError("Enemy type must be a string.")

    if not isinstance(name, str):
        raise TypeError("Enemy name must be a string.")

    enemy_name = name.strip()

    if not enemy_name.replace(" ", "").isalpha():
        raise ValueError("Enemy name must contain only letters and spaces.")

    enemy_class = ENEMY_CLASSES.get(enemy_type.strip().lower())

    if enemy_class is None:
        raise ValueError(f"Unknown enemy type: '{enemy_type}'.")

    return enemy_class(enemy_name)