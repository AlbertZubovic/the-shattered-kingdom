
import inspect

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.player import Player
from the_shattered_kingdom.inventory import Inventory
from the_shattered_kingdom.items.health_potion import HealthPotion


class DummyPlayer(Player):
    """Concrete player used for testing."""

    def introduce(self) -> None:
        pass


@pytest.fixture
def player() -> DummyPlayer:
    return DummyPlayer("Arin", 100, 20, 10)


def test_player_is_abstract() -> None:
    assert inspect.isabstract(Player)


def test_player_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match="abstract class"):
        Player("Arin", 100, 20, 10)


def test_concrete_player_can_be_instantiated(
    player: DummyPlayer,
) -> None:
    assert isinstance(player, Player)
    assert isinstance(player, Character)


def test_player_inherits_character_stats(
    player: DummyPlayer,
) -> None:
    assert player.name == "Arin"
    assert player.max_hp == 100
    assert player.hp == 100
    assert player.attack == 20
    assert player.defense == 10


def test_player_has_inventory(player: DummyPlayer) -> None:
    assert isinstance(player.inventory, Inventory)


def test_players_have_separate_inventories() -> None:
    first = DummyPlayer("Arin", 100, 20, 10)
    second = DummyPlayer("Lyra", 100, 20, 10)

    assert first.inventory is not second.inventory


def test_player_can_store_items(
    player: DummyPlayer,
    capsys: pytest.CaptureFixture[str],
) -> None:
    potion = HealthPotion("Potion", "Restores health.", 30)

    player.inventory.add_item(potion, 2)
    player.inventory.list_items()

    output = capsys.readouterr().out

    assert "Potion" in output
    assert "2" in output


def test_player_inventories_do_not_share_items() -> None:
    first = DummyPlayer("Arin", 100, 20, 10)
    second = DummyPlayer("Lyra", 100, 20, 10)

    potion = HealthPotion("Potion", "Restores health.", 30)

    first.inventory.add_item(potion, 2)

    with pytest.raises(ValueError, match="insufficient quantity"):
        second.inventory.remove_item(potion)


def test_player_inherits_combat_behavior(
    player: DummyPlayer,
) -> None:
    enemy = DummyPlayer("Enemy", 100, 10, 5)

    player.attack_target(enemy)

    assert enemy.hp == 85


def test_player_inherits_healing(
    player: DummyPlayer,
) -> None:
    damage_taken = player.take_damage(40)

    assert damage_taken == 30
    assert player.hp == 70

    total_heal = player.heal(20)

    assert total_heal == 20
    assert player.hp == 90
