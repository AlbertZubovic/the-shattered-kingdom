from typing import cast
from unittest.mock import patch

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.enemies.enemy import Enemy
from the_shattered_kingdom.characters.enemies.skeleton import Skeleton


class DummyCharacter(Character):
    """Concrete character used as a target in tests."""

    def introduce(self) -> None:
        """Implement the required abstract method."""
        pass


@pytest.fixture
def skeleton() -> Skeleton:
    return Skeleton("Bones")


def test_skeleton_starting_stats(skeleton: Skeleton) -> None:
    assert isinstance(skeleton, Enemy)
    assert isinstance(skeleton, Character)
    assert skeleton.name == "Bones"
    assert skeleton.max_hp == 95
    assert skeleton.hp == 95
    assert skeleton.attack == 25
    assert skeleton.defense == 12


def test_skeleton_introduction(skeleton: Skeleton, capsys) -> None:
    skeleton.introduce()

    output = capsys.readouterr().out

    assert "Bones" in output
    assert "Skeleton" in output
    assert "ground trembles" in output


@pytest.mark.parametrize(
    ("target_defense", "expected_damage"),
    [
        pytest.param(0, 25, id="no-defense"),
        pytest.param(10, 15, id="low-defense"),
        pytest.param(20, 5, id="high-defense"),
        pytest.param(30, 1, id="minimum-damage"),
    ],
)
def test_skeleton_life_drain_respects_defense(
    skeleton: Skeleton,
    target_defense: int,
    expected_damage: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    skeleton.special_attack(target)

    assert target.hp == 100 - expected_damage


def test_skeleton_life_drain_calls_take_damage(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 10)

    with patch.object(
        target,
        "take_damage",
        wraps=target.take_damage,
    ) as damage_spy:
        skeleton.special_attack(target)

    damage_spy.assert_called_once_with(25)
    assert target.hp == 85


@pytest.mark.parametrize(
    ("target_defense", "expected_damage", "expected_heal"),
    [
        pytest.param(0, 25, 12, id="heal-half-of-25"),
        pytest.param(5, 20, 10, id="heal-half-of-20"),
        pytest.param(10, 15, 7, id="heal-half-of-15"),
        pytest.param(20, 5, 2, id="heal-half-of-5"),
    ],
)
def test_skeleton_life_drain_heals_half_actual_damage(
    skeleton: Skeleton,
    target_defense: int,
    expected_damage: int,
    expected_heal: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    skeleton.take_damage(42)
    assert skeleton.hp == 65

    skeleton.special_attack(target)

    assert skeleton.hp == 65 + expected_heal
    assert target.hp == 100 - expected_damage


def test_skeleton_life_drain_healing_capped_at_max_hp(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    skeleton.take_damage(14)
    assert skeleton.hp == 93

    skeleton.special_attack(target)

    assert skeleton.hp == 95
    assert target.hp == 75


def test_skeleton_life_drain_at_full_hp(skeleton: Skeleton) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    skeleton.special_attack(target)

    assert skeleton.hp == 95
    assert target.hp == 75


def test_skeleton_life_drain_does_not_overheal_from_overkill(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 10, 10, 0)

    skeleton.take_damage(42)
    assert skeleton.hp == 65

    skeleton.special_attack(target)

    assert target.hp == 0
    assert skeleton.hp == 70


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_skeleton_special_attack_rejects_invalid_target(
    skeleton: Skeleton,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        skeleton.special_attack(cast(Character, invalid_target))


def test_dead_skeleton_cannot_use_special_attack(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    skeleton.take_damage(200)
    assert not skeleton.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        skeleton.special_attack(target)

    assert target.hp == 100
    assert skeleton.hp == 0


@pytest.mark.parametrize(
    ("turns", "expected_normal", "expected_special"),
    [
        pytest.param(1, 1, 0, id="first-turn-normal"),
        pytest.param(2, 1, 1, id="second-turn-life-drain"),
        pytest.param(3, 2, 1, id="third-turn-normal"),
        pytest.param(4, 2, 2, id="fourth-turn-life-drain"),
        pytest.param(6, 3, 3, id="sixth-turn-life-drain"),
        pytest.param(8, 4, 4, id="eighth-turn-life-drain"),
    ],
)
def test_skeleton_choose_action_pattern(
    skeleton: Skeleton,
    turns: int,
    expected_normal: int,
    expected_special: int,
) -> None:
    target = DummyCharacter("Enemy", 1000, 10, 0)

    with (
        patch.object(skeleton, "attack_target") as normal_attack,
        patch.object(skeleton, "special_attack") as special_attack,
    ):
        for _ in range(turns):
            skeleton.choose_action(target)

    assert normal_attack.call_count == expected_normal
    assert special_attack.call_count == expected_special


def test_skeleton_choose_action_targets_opponent(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    with (
        patch.object(skeleton, "attack_target") as normal_attack,
        patch.object(skeleton, "special_attack") as special_attack,
    ):
        for _ in range(2):
            skeleton.choose_action(target)

    normal_attack.assert_called_once_with(target)
    special_attack.assert_called_once_with(target)


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_skeleton_choose_action_rejects_invalid_target(
    skeleton: Skeleton,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        skeleton.choose_action(cast(Character, invalid_target))


def test_dead_skeleton_cannot_choose_action(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    skeleton.take_damage(200)

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        skeleton.choose_action(target)

    assert target.hp == 100


def test_invalid_action_does_not_advance_turn_counter(
    skeleton: Skeleton,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    with pytest.raises(TypeError):
        skeleton.choose_action(cast(Character, cast(object, None)))

    with (
        patch.object(skeleton, "attack_target") as normal_attack,
        patch.object(skeleton, "special_attack") as special_attack,
    ):
        skeleton.choose_action(target)

    normal_attack.assert_called_once_with(target)
    special_attack.assert_not_called()

    with patch.object(skeleton, "special_attack") as special_attack:
        skeleton.choose_action(target)

    special_attack.assert_called_once_with(target)
