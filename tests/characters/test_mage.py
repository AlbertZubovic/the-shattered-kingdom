
from typing import cast

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.mage import Mage


class DummyCharacter(Character):
    """Concrete character used as a target in tests."""

    def introduce(self) -> None:
        """Implement the required abstract method."""
        pass


@pytest.fixture
def mage() -> Mage:
    return Mage("Merlin")


def test_mage_starting_stats(mage: Mage) -> None:
    assert isinstance(mage, Character)
    assert mage.name == "Merlin"
    assert mage.max_hp == 80
    assert mage.hp == 80
    assert mage.attack == 45
    assert mage.defense == 3


def test_mage_introduction(mage: Mage, capsys) -> None:
    mage.introduce()

    output = capsys.readouterr().out

    assert "Merlin" in output
    assert "Mage" in output
    assert "Arcane energy" in output


@pytest.mark.parametrize(
    "target_defense",
    [
        pytest.param(0, id="no-defense"),
        pytest.param(10, id="low-defense"),
        pytest.param(30, id="medium-defense"),
        pytest.param(75, id="high-defense"),
    ],
)
def test_mage_fireball_ignores_defense(
    mage: Mage,
    target_defense: int,
) -> None:
    target = DummyCharacter("Enemy", 100, 10, target_defense)

    mage.special_attack(target)

    assert target.hp == 60


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Enemy", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_mage_special_attack_rejects_invalid_target(
    mage: Mage,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError):
        mage.special_attack(cast(Character, invalid_target))


def test_dead_mage_cannot_use_special_attack(mage: Mage) -> None:
    target = DummyCharacter("Enemy", 100, 10, 0)

    mage.take_damage(200)
    assert not mage.is_alive()

    with pytest.raises(ValueError, match="Dead characters cannot attack"):
        mage.special_attack(target)

    assert target.hp == 100
