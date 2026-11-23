
from typing import cast
from unittest.mock import patch

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.rogue import Rogue


class DummyCharacter(Character):
    """Concrete character used as a target in tests."""

    def introduce(self) -> None:
        """Implement the required abstract method."""
        pass


@pytest.fixture
def rogue() -> Rogue:
    return Rogue("Shadow")


def test_rogue_starting_stats(rogue: Rogue) -> None:
    assert isinstance(rogue, Character)
    assert rogue.name == "Shadow"
    assert rogue.max_hp == 100
    assert rogue.hp == 100
    assert rogue.attack == 35
    assert rogue.defense == 7


def test_rogue_introduction(rogue: Rogue, capsys) -> None:
    rogue.introduce()

    output = capsys.readouterr().out

    assert "Shadow" in output
    assert "Rogue" in output
    assert "darkness" in output


@pytest.mark.parametrize(
    ("target_defense", "expected_total_damage"),
    [
        pytest.param(0, 70, id="unarmored-target"),
        pytest.param(10, 50, id="lightly-armored-target"),
        pytest.param(20, 30, id="heavily-armored-target"),
        pytest.param(40, 2, id="minimum-damage-per-hit"),
    ],
)
def test_rogue_special_attack_damage(
    rogue: Rogue,
    target_defense: int,
    expected_total_damage: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    rogue.special_attack(target)

    assert target.hp == 100 - expected_total_damage


def test_rogue_special_attack_hits_twice(rogue: Rogue) -> None:
    target = DummyCharacter("Enemy", 100, 10, 10)

    with patch.object(
        target,
        "take_damage",
        wraps=target.take_damage,
    ) as damage_spy:
        rogue.special_attack(target)

    assert damage_spy.call_count == 2
    assert damage_spy.call_args_list[0].args == (35,)
    assert damage_spy.call_args_list[1].args == (35,)
    assert target.hp == 50


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_rogue_special_attack_rejects_invalid_target(
    rogue: Rogue,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        rogue.special_attack(cast(Character, invalid_target))


def test_dead_rogue_cannot_use_special_attack(rogue: Rogue) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    rogue.take_damage(200)
    assert not rogue.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        rogue.special_attack(target)

    assert target.hp == 100
