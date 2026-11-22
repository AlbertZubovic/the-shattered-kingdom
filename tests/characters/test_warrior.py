from typing import cast

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.warrior import Warrior


@pytest.fixture
def warrior() -> Warrior:
    return Warrior("Arin")


def test_warrior_starting_stats(warrior: Warrior) -> None:
    assert isinstance(warrior, Character)
    assert warrior.name == "Arin"
    assert warrior.max_hp == 150
    assert warrior.hp == 150
    assert warrior.attack == 30
    assert warrior.defense == 20


def test_warrior_introduction(warrior: Warrior, capsys) -> None:
    warrior.introduce()

    output = capsys.readouterr().out

    assert "Arin" in output
    assert "Warrior" in output
    assert "unbreakable shield" in output


@pytest.mark.parametrize(
    ("target_defense", "expected_damage"),
    [
        pytest.param(0, 45, id="unarmored-target"),
        pytest.param(10, 35, id="lightly-armored-target"),
        pytest.param(20, 25, id="heavily-armored-target"),
        pytest.param(50, 1, id="minimum-damage"),
    ],
)
def test_warrior_special_attack_damage(
    warrior: Warrior,
    target_defense: int,
    expected_damage: int,
) -> None:
    target = Character("Enemy", 100, 10, target_defense)

    warrior.special_attack(target)

    assert target.hp == 100 - expected_damage


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_warrior_special_attack_rejects_invalid_target(
    warrior: Warrior,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        warrior.special_attack(cast(Character, invalid_target))


def test_dead_warrior_cannot_use_special_attack(warrior: Warrior) -> None:
    target = Character("Enemy", 100, 10, 0)

    warrior.take_damage(200)
    assert not warrior.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        warrior.special_attack(target)

    assert target.hp == 100
