from typing import cast
from unittest.mock import patch

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.enemies.enemy import Enemy
from the_shattered_kingdom.characters.enemies.goblin import Goblin


class DummyCharacter(Character):
    """Concrete character used as a target in tests."""

    def introduce(self) -> None:
        """Implement the required abstract method."""
        pass


@pytest.fixture
def goblin() -> Goblin:
    return Goblin("Grim")


def test_goblin_starting_stats(goblin: Goblin) -> None:
    assert isinstance(goblin, Enemy)
    assert isinstance(goblin, Character)
    assert goblin.name == "Grim"
    assert goblin.max_hp == 60
    assert goblin.hp == 60
    assert goblin.attack == 18
    assert goblin.defense == 5


def test_goblin_introduction(goblin: Goblin, capsys) -> None:
    goblin.introduce()

    output = capsys.readouterr().out

    assert "Grim" in output
    assert "Goblin" in output
    assert "wicked grin" in output


@pytest.mark.parametrize(
    "target_defense",
    [
        pytest.param(0, id="no-defense"),
        pytest.param(10, id="low-defense"),
        pytest.param(30, id="medium-defense"),
        pytest.param(75, id="high-defense"),
    ],
)
def test_goblin_dirty_trick_ignores_defense(
    goblin: Goblin,
    target_defense: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    goblin.special_attack(target)

    assert target.hp == 90


def test_goblin_dirty_trick_calls_take_damage(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 20)

    with patch.object(
        target,
        "take_damage",
        wraps=target.take_damage,
    ) as damage_spy:
        goblin.special_attack(target)

    damage_spy.assert_called_once_with(30)
    assert target.hp == 90


def test_goblin_dirty_trick_heals_five_hp(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    damage_taken = goblin.take_damage(25)

    assert damage_taken == 20
    assert goblin.hp == 40

    total_heal = 0

    with patch.object(
        goblin,
        "heal",
        wraps=goblin.heal,
    ) as heal_spy:
        goblin.special_attack(target)

        heal_spy.assert_called_once_with(5)
        total_heal = heal_spy.return_value

    assert goblin.hp == 45
    assert target.hp == 90


def test_goblin_dirty_trick_healing_capped_at_max_hp(
    goblin: Goblin,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    goblin.take_damage(7)
    assert goblin.hp == 58

    goblin.special_attack(target)

    assert goblin.hp == 60
    assert target.hp == 90


def test_goblin_dirty_trick_at_full_hp(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    goblin.special_attack(target)

    assert goblin.hp == 60
    assert target.hp == 90


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_goblin_special_attack_rejects_invalid_target(
    goblin: Goblin,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        goblin.special_attack(cast(Character, invalid_target))


def test_dead_goblin_cannot_use_special_attack(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    goblin.take_damage(100)
    assert not goblin.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        goblin.special_attack(target)

    assert target.hp == 100
    assert goblin.hp == 0


@pytest.mark.parametrize(
    ("turns", "expected_normal", "expected_special"),
    [
        pytest.param(1, 1, 0, id="first-turn-normal"),
        pytest.param(2, 2, 0, id="second-turn-normal"),
        pytest.param(3, 2, 1, id="third-turn-dirty-trick"),
        pytest.param(4, 3, 1, id="fourth-turn-normal"),
        pytest.param(6, 4, 2, id="sixth-turn-dirty-trick"),
        pytest.param(9, 6, 3, id="ninth-turn-dirty-trick"),
    ],
)
def test_goblin_choose_action_pattern(
    goblin: Goblin,
    turns: int,
    expected_normal: int,
    expected_special: int,
) -> None:
    target = DummyCharacter("Enemy", 1000, 10, 0)

    with (
        patch.object(goblin, "attack_target") as normal_attack,
        patch.object(goblin, "special_attack") as special_attack,
    ):
        for _ in range(turns):
            goblin.choose_action(target)

    assert normal_attack.call_count == expected_normal
    assert special_attack.call_count == expected_special


def test_goblin_choose_action_targets_opponent(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    with (
        patch.object(goblin, "attack_target") as normal_attack,
        patch.object(goblin, "special_attack") as special_attack,
    ):
        for _ in range(3):
            goblin.choose_action(target)

    assert normal_attack.call_count == 2
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
def test_goblin_choose_action_rejects_invalid_target(
    goblin: Goblin,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        goblin.choose_action(cast(Character, invalid_target))


def test_dead_goblin_cannot_choose_action(goblin: Goblin) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    goblin.take_damage(100)

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        goblin.choose_action(target)

    assert target.hp == 100


def test_invalid_action_does_not_advance_turn_counter(
    goblin: Goblin,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    with pytest.raises(TypeError):
        goblin.choose_action(cast(Character, cast(object, None)))

    with (
        patch.object(goblin, "attack_target") as normal_attack,
        patch.object(goblin, "special_attack") as special_attack,
    ):
        for _ in range(2):
            goblin.choose_action(target)

    assert normal_attack.call_count == 2
    special_attack.assert_not_called()

    with patch.object(goblin, "special_attack") as special_attack:
        goblin.choose_action(target)

    special_attack.assert_called_once_with(target)
