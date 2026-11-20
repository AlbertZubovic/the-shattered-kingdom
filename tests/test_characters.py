import pytest

from src.the_shattered_kingdom.characters import Character


@pytest.fixture
def init_characters() -> Character:
    return Character("Arin", 100, 10, 5)


@pytest.mark.parametrize(
    "damage_amount, expected_hp, expected_alive",
    [
        pytest.param(20, 80, True, id="damage-20-hp"),
        pytest.param(90, 10, True, id="damage-90-hp"),
        pytest.param(100, 0, False, id="damage-to-max-hp"),
        pytest.param(200, 0, False, id="damage-over-max-hp"),
    ],
)
def test_take_damage(
    damage_amount: int,
    expected_hp: int,
    expected_alive: bool,
    init_characters: Character,
) -> None:
    arin = init_characters

    survived = arin.take_damage(damage_amount)

    assert arin.hp == expected_hp
    assert survived is expected_alive


@pytest.mark.parametrize(
    "damage_amount",
    [
        pytest.param(-10, id="damage-negative-hp"),
        pytest.param(0, id="damage-zero-hp"),
    ],
)
def test_take_damage_invalid_amount(
    damage_amount: int,
    init_characters: Character,
) -> None:
    arin = init_characters

    with pytest.raises(ValueError):
        arin.take_damage(damage_amount)


@pytest.mark.parametrize(
    "heal_amount, expected",
    [
        pytest.param(20, 70, id="heal-20-hp"),
        pytest.param(1, 51, id="heal-1-hp"),
        pytest.param(50, 100, id="heal-to-full-hp"),
        pytest.param(200, 100, id="heal-over-max-hp"),
    ],
)
def test_heal(
    heal_amount: int,
    expected: int,
    init_characters: Character,
) -> None:
    arin = init_characters
    arin.take_damage(50)

    arin.heal(heal_amount)

    assert arin.hp == expected


@pytest.mark.parametrize(
    "heal_amount",
    [
        pytest.param(-10, id="heal-negative-hp"),
        pytest.param(0, id="heal-zero-hp"),
    ],
)
def test_heal_invalid_amount(
    heal_amount: int,
    init_characters: Character,
) -> None:
    arin = init_characters
    arin.take_damage(50)

    with pytest.raises(ValueError):
        arin.heal(heal_amount)


@pytest.mark.parametrize(
    "damage_taken, expected",
    [
        pytest.param(20, True, id="alive-after-20-damage"),
        pytest.param(50, True, id="alive-after-50-damage"),
        pytest.param(200, False, id="dead-after-200-damage"),
        pytest.param(100, False, id="dead-after-100-damage"),
    ],
)
def test_is_alive(
    init_characters: Character,
    damage_taken: int,
    expected: bool,
) -> None:
    arin = init_characters
    arin.take_damage(damage_taken)

    assert arin.is_alive() is expected


@pytest.mark.parametrize(
    "name, max_hp, attack, defense, expected_exception",
    [
        pytest.param(
            "", 100, 10, 5, ValueError,
            id="empty-name",
        ),
        pytest.param(
            "   ", 100, 10, 5, ValueError,
            id="whitespace-only-name",
        ),
        pytest.param(
            123, 100, 10, 5, TypeError,
            id="name-not-string",
        ),
        pytest.param(
            "Arin", 0, 10, 5, ValueError,
            id="zero-max-hp",
        ),
        pytest.param(
            "Arin", -10, 10, 5, ValueError,
            id="negative-max-hp",
        ),
        pytest.param(
            "Arin", "100", 10, 5, TypeError,
            id="max-hp-not-integer",
        ),
        pytest.param(
            "Arin", True, 10, 5, TypeError,
            id="max-hp-boolean",
        ),
        pytest.param(
            "Arin", 100, -5, 5, ValueError,
            id="negative-attack",
        ),
        pytest.param(
            "Arin", 100, "10", 5, TypeError,
            id="attack-not-integer",
        ),
        pytest.param(
            "Arin", 100, True, 5, TypeError,
            id="attack-boolean",
        ),
        pytest.param(
            "Arin", 100, 10, -5, ValueError,
            id="negative-defense",
        ),
        pytest.param(
            "Arin", 100, 10, "5", TypeError,
            id="defense-not-integer",
        ),
        pytest.param(
            "Arin", 100, 10, True, TypeError,
            id="defense-boolean",
        ),
    ],
)
def test_character_invalid_initialization(
    name: object,
    max_hp: object,
    attack: object,
    defense: object,
    expected_exception: type[Exception],
) -> None:
    with pytest.raises(expected_exception):
        Character(name, max_hp, attack, defense)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "name, expected_name",
    [
        pytest.param("Arin", "Arin", id="normal-name"),
        pytest.param("  Arin  ", "Arin", id="trim-name-whitespace"),
        pytest.param("A", "A", id="single-character-name"),
    ],
)
def test_character_name(
    name: str,
    expected_name: str,
) -> None:
    character = Character(name, 100, 10, 5)

    assert character.name == expected_name


def test_character_initial_stats(init_characters: Character) -> None:
    arin = init_characters

    assert arin.name == "Arin"
    assert arin.max_hp == 100
    assert arin.hp == 100
    assert arin.attack == 10
    assert arin.defense == 5
    assert arin.is_alive() is True


def test_heal_dead_character(init_characters: Character) -> None:
    arin = init_characters
    arin.take_damage(100)

    arin.heal(50)

    assert arin.hp == 0
    assert arin.is_alive() is False


def test_independent_character_state() -> None:
    arin = Character("Arin", 100, 10, 5)
    quake = Character("Quake", 150, 25, 15)

    arin.take_damage(40)

    assert arin.hp == 60
    assert quake.hp == 150


def test_character_string_representation(
    init_characters: Character,
) -> None:
    arin = init_characters

    assert str(arin) == (
        "Hero: Arin | HP: 100/100 | ATK: 10 | DEF: 5"
    )
