
from unittest.mock import patch

import pytest

from src.the_shattered_kingdom.battle import Battle
from the_shattered_kingdom.characters.character import Character


@pytest.fixture
def initiate_battle() -> tuple[Battle, Character, Character]:
    arin = Character("Arin", 100, 50, 10)
    quake = Character("Quake", 100, 20, 15)

    return Battle(arin, quake), arin, quake


@pytest.mark.parametrize(
    "invalid_position, invalid_value",
    [
        pytest.param("first", None, id="first-combatant-none"),
        pytest.param("first", "Arin", id="first-combatant-string"),
        pytest.param("first", 123, id="first-combatant-integer"),
        pytest.param("second", None, id="second-combatant-none"),
        pytest.param("second", "Quake", id="second-combatant-string"),
        pytest.param("second", 123, id="second-combatant-integer"),
    ],
)
def test_battle_invalid_combatant_types(
    invalid_position: str,
    invalid_value: object,
) -> None:
    arin = Character("Arin", 100, 10, 5)
    quake = Character("Quake", 100, 10, 5)

    if invalid_position == "first":
        with pytest.raises(TypeError):
            Battle(invalid_value, quake)  # type: ignore[arg-type]
    else:
        with pytest.raises(TypeError):
            Battle(arin, invalid_value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "dead_combatant",
    [
        pytest.param("first", id="first-combatant-dead"),
        pytest.param("second", id="second-combatant-dead"),
        pytest.param("both", id="both-combatants-dead"),
    ],
)
def test_battle_rejects_dead_combatants(
    dead_combatant: str,
) -> None:
    arin = Character("Arin", 100, 10, 5)
    quake = Character("Quake", 100, 10, 5)

    if dead_combatant in ("first", "both"):
        arin.take_damage(105)

    if dead_combatant in ("second", "both"):
        quake.take_damage(105)

    if dead_combatant in ("first", "both"):
        assert not arin.is_alive()

    if dead_combatant in ("second", "both"):
        assert not quake.is_alive()

    with pytest.raises(ValueError):
        Battle(arin, quake)


def test_battle_rejects_same_character() -> None:
    arin = Character("Arin", 100, 10, 5)

    with pytest.raises(ValueError):
        Battle(arin, arin)


@pytest.mark.parametrize(
    (
        "a_hp, a_attack, a_defense, "
        "b_hp, b_attack, b_defense, expected_winner"
    ),
    [
        pytest.param(
            100, 50, 10,
            100, 20, 15,
            "Arin",
            id="first-combatant-wins",
        ),
        pytest.param(
            50, 10, 0,
            100, 100, 0,
            "Quake",
            id="second-combatant-wins",
        ),
        pytest.param(
            20, 20, 0,
            20, 20, 0,
            "Arin",
            id="equal-stats-first-attacker-wins",
        ),
        pytest.param(
            10, 10, 0,
            10, 0, 100,
            "Arin",
            id="minimum-damage-eventual-win",
        ),
        pytest.param(
            100, 0, 100,
            2, 0, 100,
            "Arin",
            id="both-attacks-zero-minimum-damage",
        ),
    ],
)
def test_battle_returns_expected_winner(
    a_hp: int,
    a_attack: int,
    a_defense: int,
    b_hp: int,
    b_attack: int,
    b_defense: int,
    expected_winner: str,
) -> None:
    arin = Character("Arin", a_hp, a_attack, a_defense)
    quake = Character("Quake", b_hp, b_attack, b_defense)

    battle = Battle(arin, quake)

    winner = battle.start_battle()

    assert isinstance(winner, Character)
    assert winner.name == expected_winner
    assert winner.is_alive() is True

    loser = quake if winner is arin else arin

    assert loser.hp == 0
    assert loser.is_alive() is False


@pytest.mark.parametrize(
    "attack, defense",
    [
        pytest.param(20, 0, id="exact-lethal-hit"),
        pytest.param(100, 0, id="overkill-hit"),
        pytest.param(25, 5, id="exact-lethal-after-defense"),
    ],
)
def test_battle_ends_on_first_lethal_attack(
    attack: int,
    defense: int,
) -> None:
    arin = Character("Arin", 100, attack, 0)
    quake = Character("Quake", 20, 100, defense)

    battle = Battle(arin, quake)

    with patch.object(
        quake,
        "attack_target",
        wraps=quake.attack_target,
    ) as quake_attack:
        winner = battle.start_battle()

    assert winner is arin
    assert quake.hp == 0
    assert arin.hp == 100

    quake_attack.assert_not_called()


def test_battle_first_combatant_attacks_first(
    initiate_battle: tuple[Battle, Character, Character],
) -> None:
    battle, arin, quake = initiate_battle

    with (
        patch.object(
            arin,
            "attack_target",
            wraps=arin.attack_target,
        ) as arin_attack,
        patch.object(
            quake,
            "attack_target",
            wraps=quake.attack_target,
        ) as quake_attack,
    ):
        winner = battle.start_battle()

    assert winner is arin
    assert arin_attack.call_count == 3
    assert quake_attack.call_count == 2


def test_turn_order(
    initiate_battle: tuple[Battle, Character, Character],
) -> None:
    battle, arin, quake = initiate_battle

    attack_order: list[str] = []

    original_arin_attack = arin.attack_target
    original_quake_attack = quake.attack_target

    def attack_quake(target: Character) -> None:
        attack_order.append("Arin")
        original_arin_attack(target)

    def attack_arin(target: Character) -> None:
        attack_order.append("Quake")
        original_quake_attack(target)

    with (
        patch.object(
            arin,
            "attack_target",
            side_effect=attack_quake,
        ),
        patch.object(
            quake,
            "attack_target",
            side_effect=attack_arin,
        ),
    ):
        winner = battle.start_battle()

    assert winner is arin

    assert attack_order == [
        "Arin",
        "Quake",
        "Arin",
        "Quake",
        "Arin",
    ]

    for i, attacker in enumerate(attack_order):
        expected = "Arin" if i % 2 == 0 else "Quake"
        assert attacker == expected


def test_battle_stops_after_combatant_dies() -> None:
    arin = Character("Arin", 100, 100, 0)
    quake = Character("Quake", 50, 10, 0)

    battle = Battle(arin, quake)

    with (
        patch.object(
            arin,
            "attack_target",
            wraps=arin.attack_target,
        ) as arin_attack,
        patch.object(
            quake,
            "attack_target",
            wraps=quake.attack_target,
        ) as quake_attack,
    ):
        winner = battle.start_battle()

    assert winner is arin
    assert arin_attack.call_count == 1
    quake_attack.assert_not_called()

    assert arin.hp == 100
    assert quake.hp == 0


def test_battle_cannot_restart(
    initiate_battle: tuple[Battle, Character, Character],
) -> None:
    battle, arin, _ = initiate_battle

    winner = battle.start_battle()

    assert winner is arin

    with pytest.raises(RuntimeError):
        battle.start_battle()


def test_battle_restart_does_not_change_character_state(
    initiate_battle: tuple[Battle, Character, Character],
) -> None:
    battle, arin, quake = initiate_battle

    battle.start_battle()

    arin_hp = arin.hp
    quake_hp = quake.hp

    with pytest.raises(RuntimeError):
        battle.start_battle()

    assert arin.hp == arin_hp
    assert quake.hp == quake_hp


def test_battle_does_not_modify_combatant_stats(
    initiate_battle: tuple[Battle, Character, Character],
) -> None:
    battle, arin, quake = initiate_battle

    battle.start_battle()

    assert arin.max_hp == 100
    assert arin.attack == 50
    assert arin.defense == 10

    assert quake.max_hp == 100
    assert quake.attack == 20
    assert quake.defense == 15
