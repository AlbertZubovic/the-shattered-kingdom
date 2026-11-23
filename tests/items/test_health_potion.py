
from typing import cast

import pytest

from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.items.health_potion import HealthPotion
from the_shattered_kingdom.items.item import Item


class DummyCharacter(Character):
    """Concrete character used as a potion target."""

    def introduce(self) -> None:
        pass


@pytest.fixture
def potion() -> HealthPotion:
    return HealthPotion("Potion", "Restores health.", 30)


def test_health_potion_is_an_item(potion: HealthPotion) -> None:
    assert isinstance(potion, Item)


def test_health_potion_heals_target(potion: HealthPotion) -> None:
    target = DummyCharacter("Arin", 100, 20, 5)

    target.take_damage(45)
    assert target.hp == 60

    potion.item_action(target)

    assert target.hp == 90


def test_health_potion_cannot_exceed_max_hp(
    potion: HealthPotion,
) -> None:
    target = DummyCharacter("Arin", 100, 20, 5)

    target.take_damage(15)
    assert target.hp == 90

    potion.item_action(target)

    assert target.hp == 100


def test_health_potion_at_full_hp(potion: HealthPotion) -> None:
    target = DummyCharacter("Arin", 100, 20, 5)

    potion.item_action(target)

    assert target.hp == 100


def test_health_potion_cannot_revive_dead_character(
    potion: HealthPotion,
) -> None:
    target = DummyCharacter("Arin", 100, 20, 5)

    target.take_damage(200)
    assert not target.is_alive()

    potion.item_action(target)

    assert target.hp == 0


def test_health_potion_prints_actual_healing(
    potion: HealthPotion,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = DummyCharacter("Arin", 100, 20, 5)

    target.take_damage(15)
    capsys.readouterr()

    potion.item_action(target)

    output = capsys.readouterr().out

    assert "Arin" in output
    assert "10" in output


@pytest.mark.parametrize(
    "heal_amount",
    [
        pytest.param(1, id="minimum"),
        pytest.param(30, id="normal"),
        pytest.param(100, id="large"),
    ],
)
def test_health_potion_accepts_positive_healing(
    heal_amount: int,
) -> None:
    potion = HealthPotion("Potion", "Restores health.", heal_amount)
    target = DummyCharacter("Arin", 200, 20, 0)

    target.take_damage(150)
    potion.item_action(target)

    assert target.hp == 50 + heal_amount


@pytest.mark.parametrize(
    "heal_amount",
    [
        pytest.param(0, id="zero"),
        pytest.param(-5, id="negative"),
    ],
)
def test_health_potion_rejects_nonpositive_healing(
    heal_amount: int,
) -> None:
    with pytest.raises(ValueError, match="Heal amount must be greater than 0"):
        HealthPotion("Potion", "Restores health.", heal_amount)


@pytest.mark.parametrize(
    "heal_amount",
    [
        pytest.param(None, id="none"),
        pytest.param(3.5, id="float"),
        pytest.param(True, id="boolean"),
        pytest.param("30", id="string"),
    ],
)
def test_health_potion_rejects_invalid_heal_types(
    heal_amount: object,
) -> None:
    with pytest.raises(TypeError, match="Heal amount must be a number"):
        HealthPotion(
            "Potion",
            "Restores health.",
            heal_amount,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_target",
    [
        pytest.param(None, id="none"),
        pytest.param("Arin", id="string"),
        pytest.param(42, id="integer"),
    ],
)
def test_health_potion_rejects_invalid_targets(
    potion: HealthPotion,
    invalid_target: object,
) -> None:
    with pytest.raises(TypeError, match="The target is not a Character"):
        potion.item_action(cast(Character, invalid_target))
