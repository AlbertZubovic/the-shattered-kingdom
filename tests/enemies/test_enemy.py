import inspect

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.enemies.enemy import Enemy


class DummyEnemy(Enemy):
    """Concrete enemy used to test inherited behavior."""

    def introduce(self) -> None:
        """Implement the required introduction method."""
        pass

    def choose_action(self, target: Character) -> None:
        """Implement the required action-selection method."""
        pass


class IncompleteEnemy(Enemy):
    """Enemy that implements introduce but not choose_action."""

    def introduce(self) -> None:
        """Implement the required introduction method."""
        pass


def test_enemy_is_abstract() -> None:
    assert inspect.isabstract(Enemy)


def test_enemy_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match="abstract class"):
        Enemy("Goblin", 60, 18, 5)


def test_enemy_requires_choose_action() -> None:
    with pytest.raises(TypeError, match="choose_action"):
        IncompleteEnemy("Goblin", 60, 18, 5)


def test_concrete_enemy_can_be_instantiated() -> None:
    enemy = DummyEnemy("Goblin", 60, 18, 5)

    assert isinstance(enemy, Enemy)
    assert isinstance(enemy, Character)


def test_enemy_inherits_character_stats() -> None:
    enemy = DummyEnemy("Goblin", 60, 18, 5)

    assert enemy.name == "Goblin"
    assert enemy.max_hp == 60
    assert enemy.hp == 60
    assert enemy.attack == 18
    assert enemy.defense == 5


def test_enemy_inherits_character_combat_behavior() -> None:
    enemy = DummyEnemy("Goblin", 60, 18, 5)
    target = DummyEnemy("Skeleton", 100, 20, 10)

    enemy.attack_target(target)

    assert target.hp == 92
    assert enemy.hp == 60


def test_enemy_inherits_damage_and_healing() -> None:
    enemy = DummyEnemy("Goblin", 60, 18, 5)

    damage_taken = enemy.take_damage(25)

    assert damage_taken == 20
    assert enemy.hp == 40

    total_heal = enemy.heal(10)

    assert total_heal == 10
    assert enemy.hp == 50
    assert enemy.is_alive() is True
