from unittest.mock import patch

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.mage import Mage
from the_shattered_kingdom.characters.rogue import Rogue
from the_shattered_kingdom.characters.warrior import Warrior
from the_shattered_kingdom.main import create_hero, start


@pytest.mark.parametrize(
    ("selection", "expected_class"),
    [
        pytest.param("1", Warrior, id="select-warrior"),
        pytest.param("2", Mage, id="select-mage"),
        pytest.param("3", Rogue, id="select-rogue"),
    ],
)
def test_create_hero_valid_selection(
    selection: str,
    expected_class: type[Character],
) -> None:
    with patch("builtins.input", side_effect=["Alice", selection]):
        hero = create_hero()

    assert type(hero) is expected_class
    assert hero.name == "Alice"


@pytest.mark.parametrize(
    ("invalid_selection", "valid_selection", "expected_class"),
    [
        pytest.param("0", "1", Warrior, id="selection-below-range"),
        pytest.param("4", "2", Mage, id="selection-above-range"),
        pytest.param("9", "3", Rogue, id="selection-out-of-range"),
        pytest.param("-1", "1", Warrior, id="negative-selection"),
    ],
)
def test_create_hero_retries_invalid_selection(
    invalid_selection: str,
    valid_selection: str,
    expected_class: type[Character],
) -> None:
    with patch(
        "builtins.input",
        side_effect=["Alice", invalid_selection, valid_selection],
    ) as input_mock:
        hero = create_hero()

    assert type(hero) is expected_class
    assert hero.name == "Alice"
    assert input_mock.call_count == 3


@pytest.mark.parametrize(
    ("invalid_selection", "valid_selection", "expected_class"),
    [
        pytest.param("abc", "1", Warrior, id="alphabetic-input"),
        pytest.param("", "2", Mage, id="empty-input"),
        pytest.param("1.5", "3", Rogue, id="decimal-input"),
        pytest.param("!", "1", Warrior, id="symbol-input"),
    ],
)
def test_create_hero_retries_non_numeric_selection(
    invalid_selection: str,
    valid_selection: str,
    expected_class: type[Character],
) -> None:
    with patch(
        "builtins.input",
        side_effect=["Alice", invalid_selection, valid_selection],
    ) as input_mock:
        hero = create_hero()

    assert type(hero) is expected_class
    assert hero.name == "Alice"
    assert input_mock.call_count == 3


@pytest.mark.parametrize(
    "invalid_name",
    [
        pytest.param("", id="empty-name"),
        pytest.param("Alice123", id="alphanumeric-name"),
        pytest.param("Alice Smith", id="name-with-spaces"),
        pytest.param("Alice!", id="name-with-symbol"),
        pytest.param("123", id="numeric-name"),
    ],
)
def test_create_hero_rejects_invalid_name(
    invalid_name: str,
) -> None:
    with patch("builtins.input", return_value=invalid_name) as input_mock:
        with pytest.raises(
            ValueError,
            match="Hero name must only contain characters",
        ):
            create_hero()

    assert input_mock.call_count == 1


@pytest.mark.parametrize(
    ("selection", "expected_class"),
    [
        pytest.param("1", Warrior, id="warrior"),
        pytest.param("2", Mage, id="mage"),
        pytest.param("3", Rogue, id="rogue"),
    ],
)
def test_start_introduces_selected_hero(
    selection: str,
    expected_class: type[Character],
    capsys: pytest.CaptureFixture[str],
) -> None:
    with (
        patch("builtins.input", side_effect=["Alice", selection]),
        patch.object(expected_class, "introduce", autospec=True) as introduce_mock,
    ):
        start()

    introduce_mock.assert_called_once()

    introduced_hero = introduce_mock.call_args.args[0]

    assert type(introduced_hero) is expected_class
    assert introduced_hero.name == "Alice"

    output = capsys.readouterr().out
    assert "Welcome to The Shattered Kingdom!" in output
