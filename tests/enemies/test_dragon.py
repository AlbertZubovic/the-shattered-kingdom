
from typing import cast
from unittest.mock import patch

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.enemies.dragon import Dragon
from the_shattered_kingdom.enemies.enemy import Enemy


class DummyCharacter(Character):
    """Concrete character used as a target in tests."""

    def introduce(self) -> None:
        """Implement the required abstract method."""
        pass


@pytest.fixture
def dragon() -> Dragon:
    return Dragon("Smaug")


def test_dragon_starting_stats(dragon: Dragon) -> None:
    assert isinstance(dragon, Enemy)
    assert isinstance(dragon, Character)
    assert dragon.name == "Smaug"
    assert dragon.max_hp == 220
    assert dragon.hp == 220
    assert dragon.attack == 40
    assert dragon.defense == 18


def test_dragon_introduction(dragon: Dragon, capsys) -> None:
    dragon.introduce()

    output = capsys.readouterr().out

    assert "Smaug" in output
    assert "Dragon" in output
    assert "skies darken" in output


@pytest.mark.parametrize(
    "target_defense",
    [
        pytest.param(0, id="no-defense"),
        pytest.param(10, id="low-defense"),
        pytest.param(30, id="medium-defense"),
        pytest.param(75, id="high-defense"),
    ],
)
def test_dragon_inferno_ignores_defense(
    dragon: Dragon,
    target_defense: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    dragon.special_attack(target)

    assert target.hp == 50


def test_dragon_inferno_calls_take_damage(dragon: Dragon) -> None:
    target = DummyCharacter("Enemy", 100, 10, 20)

    with patch.object(
        target,
        "take_damage",
        wraps=target.take_damage,
    ) as damage_spy:
        dragon.special_attack(target)

    damage_spy.assert_called_once_with(70)
    assert target.hp == 50


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_dragon_special_attack_rejects_invalid_target(
    dragon: Dragon,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        dragon.special_attack(cast(Character, invalid_target))


def test_dead_dragon_cannot_use_special_attack(dragon: Dragon) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    dragon.take_damage(300)
    assert not dragon.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        dragon.special_attack(target)

    assert target.hp == 100


@pytest.mark.parametrize(
    ("turns", "expected_normal", "expected_special"),
    [
        pytest.param(1, 1, 0, id="first-turn-normal"),
        pytest.param(2, 2, 0, id="second-turn-normal"),
        pytest.param(3, 3, 0, id="third-turn-normal"),
        pytest.param(4, 3, 1, id="fourth-turn-inferno"),
        pytest.param(5, 4, 1, id="fifth-turn-normal"),
        pytest.param(8, 6, 2, id="eighth-turn-inferno"),
    ],
)
def test_dragon_choose_action_pattern(
    dragon: Dragon,
    turns: int,
    expected_normal: int,
    expected_special: int,
) -> None:
    target = DummyCharacter("Enemy", 1000, 10, 0)

    with (
        patch.object(dragon, "attack_target") as normal_attack,
        patch.object(dragon, "special_attack") as special_attack,
    ):
        for _ in range(turns):
            dragon.choose_action(target)

    assert normal_attack.call_count == expected_normal
    assert special_attack.call_count == expected_special


def test_dragon_choose_action_targets_opponent(dragon: Dragon) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    with (
        patch.object(dragon, "attack_target") as normal_attack,
        patch.object(dragon, "special_attack") as special_attack,
    ):
        for _ in range(4):
            dragon.choose_action(target)

    assert normal_attack.call_count == 3
    assert special_attack.call_count == 1

    normal_attack.assert_called_with(target)
    special_attack.assert_called_once_with(target)


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_dragon_choose_action_rejects_invalid_target(
    dragon: Dragon,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        dragon.choose_action(cast(Character, invalid_target))


def test_dead_dragon_cannot_choose_action(dragon: Dragon) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    dragon.take_damage(300)

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        dragon.choose_action(target)

    assert target.hp == 100


def test_invalid_action_does_not_advance_turn_counter(
    dragon: Dragon,
) -> None:
    target = DummyCharacter("Enemy", 1000, 10, 0)

    with pytest.raises(TypeError):
        dragon.choose_action(cast(Character, cast(object, None)))

    with (
        patch.object(dragon, "attack_target") as normal_attack,
        patch.object(dragon, "special_attack") as special_attack,
    ):
        for _ in range(3):
            dragon.choose_action(target)

    assert normal_attack.call_count == 3
    special_attack.assert_not_called()

    with patch.object(dragon, "special_attack") as special_attack:
        dragon.choose_action(target)

    special_attack.assert_called_once_with(target)
