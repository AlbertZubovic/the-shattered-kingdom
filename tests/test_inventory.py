
import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.inventory import Inventory
from the_shattered_kingdom.items.item import Item


class DummyItem(Item):
    """Concrete item used for inventory tests."""

    def item_action(self, target: Character) -> None:
        pass


@pytest.fixture
def inventory() -> Inventory:
    return Inventory()


@pytest.fixture
def potion() -> DummyItem:
    return DummyItem("Potion", "Restores health.")


def test_inventory_starts_empty(
    inventory: Inventory,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.list_items()

    assert "Inventory is empty." in capsys.readouterr().out


def test_inventory_adds_item(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion)

    inventory.list_items()
    output = capsys.readouterr().out

    assert "Potion" in output
    assert "1" in output


def test_inventory_adds_multiple_items(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion, 3)

    inventory.list_items()
    output = capsys.readouterr().out

    assert "Potion" in output
    assert "3" in output


def test_inventory_stacks_same_item(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion, 2)
    inventory.add_item(potion, 3)

    inventory.list_items()
    output = capsys.readouterr().out

    assert "Potion" in output
    assert "5" in output


def test_inventory_stores_different_items(
    inventory: Inventory,
    capsys: pytest.CaptureFixture[str],
) -> None:
    potion = DummyItem("Potion", "Restores health.")
    sword = DummyItem("Sword", "A sharp weapon.")

    inventory.add_item(potion, 2)
    inventory.add_item(sword, 1)

    inventory.list_items()
    output = capsys.readouterr().out

    assert "Potion" in output
    assert "Sword" in output


def test_inventory_removes_item(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion, 5)
    inventory.remove_item(potion, 2)

    inventory.list_items()
    output = capsys.readouterr().out

    assert "Potion" in output
    assert "3" in output


def test_inventory_removes_item_completely(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion, 2)
    inventory.remove_item(potion, 2)

    inventory.list_items()

    assert "Inventory is empty." in capsys.readouterr().out


def test_inventory_clears_items(
    inventory: Inventory,
    potion: DummyItem,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inventory.add_item(potion, 5)
    inventory.clear_inventory()

    inventory.list_items()

    assert "Inventory is empty." in capsys.readouterr().out


@pytest.mark.parametrize(
    "amount",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(1.5, id="float"),
        pytest.param(True, id="boolean"),
        pytest.param("2", id="string"),
    ],
)
def test_inventory_rejects_invalid_add_amount(
    inventory: Inventory,
    potion: DummyItem,
    amount: object,
) -> None:
    with pytest.raises(ValueError, match="Amount must be a positive integer"):
        inventory.add_item(potion, amount)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "amount",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(1.5, id="float"),
        pytest.param(True, id="boolean"),
        pytest.param("2", id="string"),
    ],
)
def test_inventory_rejects_invalid_remove_amount(
    inventory: Inventory,
    potion: DummyItem,
    amount: object,
) -> None:
    inventory.add_item(potion, 5)

    with pytest.raises(ValueError, match="Amount must be a positive integer"):
        inventory.remove_item(potion, amount)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "invalid_item",
    [
        pytest.param(None, id="none"),
        pytest.param("Potion", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_inventory_rejects_invalid_items(
    inventory: Inventory,
    invalid_item: object,
) -> None:
    with pytest.raises(TypeError, match="Item is not a valid item"):
        inventory.add_item(invalid_item)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="Item is not a valid item"):
        inventory.remove_item(invalid_item)  # type: ignore[arg-type]


def test_inventory_cannot_remove_missing_item(
    inventory: Inventory,
    potion: DummyItem,
) -> None:
    with pytest.raises(ValueError, match="insufficient quantity"):
        inventory.remove_item(potion)


def test_inventory_cannot_remove_more_than_owned(
    inventory: Inventory,
    potion: DummyItem,
) -> None:
    inventory.add_item(potion, 2)

    with pytest.raises(ValueError, match="insufficient quantity"):
        inventory.remove_item(potion, 3)


def test_inventories_are_independent(potion: DummyItem) -> None:
    first = Inventory()
    second = Inventory()

    first.add_item(potion, 3)

    with pytest.raises(ValueError, match="insufficient quantity"):
        second.remove_item(potion)

    first.remove_item(potion, 3)

    assert first is not second
