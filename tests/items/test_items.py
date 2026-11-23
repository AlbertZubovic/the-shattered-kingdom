
import inspect

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.items.item import Item


class DummyItem(Item):
    """Concrete item used for testing."""

    def item_action(self, target: Character) -> None:
        pass


def test_item_is_abstract() -> None:
    assert inspect.isabstract(Item)


def test_item_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match="abstract class"):
        Item("Potion", "Restores health.")


def test_concrete_item_can_be_instantiated() -> None:
    item = DummyItem("Potion", "Restores health.")

    assert isinstance(item, Item)


def test_item_stores_name_and_description() -> None:
    item = DummyItem("Potion", "Restores health.")

    assert item.name == "Potion"


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="whitespace"),
    ],
)
def test_item_rejects_invalid_names(name: str) -> None:
    with pytest.raises(ValueError):
        DummyItem(name, "Restores health.")


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(None, id="none"),
        pytest.param(42, id="integer"),
        pytest.param(True, id="boolean"),
        pytest.param([], id="list"),
    ],
)
def test_item_rejects_non_string_names(name: object) -> None:
    with pytest.raises(TypeError, match="Item name must be a string"):
        DummyItem(name, "Restores health.")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "description",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="whitespace"),
    ],
)
def test_item_rejects_empty_descriptions(description: str) -> None:
    with pytest.raises(ValueError, match="Item description must not be empty"):
        DummyItem("Potion", description)


@pytest.mark.parametrize(
    "description",
    [
        pytest.param(None, id="none"),
        pytest.param(42, id="integer"),
        pytest.param(True, id="boolean"),
    ],
)
def test_item_rejects_non_string_descriptions(
    description: object,
) -> None:
    with pytest.raises(TypeError, match="Item description must be a string"):
        DummyItem("Potion", description)  # type: ignore[arg-type]
