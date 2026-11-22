import pytest

from the_shattered_kingdom.enemies.dragon import Dragon
from the_shattered_kingdom.enemies.enemy import Enemy
from the_shattered_kingdom.enemies.factory import (
    ENEMY_CLASSES,
    create_enemy,
)
from the_shattered_kingdom.enemies.goblin import Goblin
from the_shattered_kingdom.enemies.skeleton import Skeleton


@pytest.mark.parametrize(
    ("enemy_type", "enemy_class", "expected_stats"),
    [
        pytest.param(
            "dragon", Dragon, (220, 40, 18), id="dragon"
        ),
        pytest.param(
            "goblin", Goblin, (60, 18, 5), id="goblin"
        ),
        pytest.param(
            "skeleton", Skeleton, (95, 25, 12), id="skeleton"
        ),
    ],
)
def test_create_enemy_returns_correct_class_and_stats(
    enemy_type: str,
    enemy_class: type[Enemy],
    expected_stats: tuple[int, int, int],
) -> None:
    enemy = create_enemy("Monster", enemy_type)

    assert isinstance(enemy, enemy_class)
    assert isinstance(enemy, Enemy)
    assert enemy.name == "Monster"
    assert (
        enemy.max_hp,
        enemy.attack,
        enemy.defense,
    ) == expected_stats

    assert enemy.hp == enemy.max_hp
    assert enemy.is_alive()


@pytest.mark.parametrize(
    ("enemy_type", "expected_class"),
    [
        pytest.param("DRAGON", Dragon, id="uppercase"),
        pytest.param("GoBlIn", Goblin, id="mixed-case"),
        pytest.param(" Skeleton ", Skeleton, id="surrounding-spaces"),
        pytest.param("  GOBLIN  ", Goblin, id="spaces-and-uppercase"),
    ],
)
def test_create_enemy_normalizes_enemy_type(
    enemy_type: str,
    expected_class: type[Enemy],
) -> None:
    enemy = create_enemy("Monster", enemy_type)

    assert isinstance(enemy, expected_class)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        pytest.param("Grim", "Grim", id="simple-name"),
        pytest.param("  Grim  ", "Grim", id="surrounding-spaces"),
        pytest.param("Dark Lord", "Dark Lord", id="multiple-words"),
        pytest.param("  Dark Lord  ", "Dark Lord", id="trim-multiple-words"),
        pytest.param("Éomer", "Éomer", id="unicode-letters"),
    ],
)
def test_create_enemy_accepts_valid_names(
    name: str,
    expected_name: str,
) -> None:
    enemy = create_enemy(name, "goblin")

    assert enemy.name == expected_name


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="whitespace-only"),
        pytest.param("Goblin123", id="numbers"),
        pytest.param("Goblin!", id="punctuation"),
        pytest.param("Dark-Lord", id="hyphen"),
        pytest.param("Dark_Lord", id="underscore"),
    ],
)
def test_create_enemy_rejects_invalid_names(name: str) -> None:
    with pytest.raises(
        ValueError,
        match="Enemy name must contain only letters and spaces",
    ):
        create_enemy(name, "goblin")


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(None, id="none"),
        pytest.param(42, id="integer"),
        pytest.param(3.14, id="float"),
        pytest.param([], id="list"),
        pytest.param(True, id="boolean"),
    ],
)
def test_create_enemy_rejects_non_string_names(name: object) -> None:
    with pytest.raises(TypeError, match="Enemy name must be a string"):
        create_enemy(name, "goblin")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "enemy_type",
    [
        pytest.param(None, id="none"),
        pytest.param(42, id="integer"),
        pytest.param(3.14, id="float"),
        pytest.param([], id="list"),
        pytest.param(True, id="boolean"),
    ],
)
def test_create_enemy_rejects_non_string_enemy_types(
    enemy_type: object,
) -> None:
    with pytest.raises(TypeError, match="Enemy type must be a string"):
        create_enemy("Monster", enemy_type)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "enemy_type",
    [
        pytest.param("orc", id="unknown-type"),
        pytest.param("", id="empty-type"),
        pytest.param("   ", id="whitespace-only"),
        pytest.param("dragon123", id="numbers"),
    ],
)
def test_create_enemy_rejects_unknown_enemy_types(
    enemy_type: str,
) -> None:
    with pytest.raises(ValueError, match="Unknown enemy type"):
        create_enemy("Monster", enemy_type)


def test_create_enemy_returns_new_instance_each_time() -> None:
    first_enemy = create_enemy("Grim", "goblin")
    second_enemy = create_enemy("Grim", "goblin")

    assert first_enemy is not second_enemy
    assert first_enemy.name == second_enemy.name

    first_enemy.take_damage(25)

    assert first_enemy.hp == 40
    assert second_enemy.hp == 60


def test_factory_registry_contains_expected_classes() -> None:
    assert ENEMY_CLASSES == {
        "dragon": Dragon,
        "goblin": Goblin,
        "skeleton": Skeleton,
    }


def test_factory_supports_new_enemy_without_changing_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Orc(Enemy):
        """Concrete enemy used to test factory extensibility."""

        def __init__(self, name: str) -> None:
            super().__init__(name, max_hp=120, attack=30, defense=15)

        def introduce(self) -> None:
            pass

        def choose_action(self, target) -> None:
            self.attack_target(target)

    monkeypatch.setitem(ENEMY_CLASSES, "orc", Orc)

    enemy = create_enemy("Grom", "orc")

    assert isinstance(enemy, Orc)
    assert isinstance(enemy, Enemy)
    assert enemy.name == "Grom"
    assert enemy.max_hp == 120
    assert enemy.attack == 30
    assert enemy.defense == 15
