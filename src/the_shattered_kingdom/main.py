from the_shattered_kingdom.characters.character import Character
from the_shattered_kingdom.characters.players.mage import Mage
from the_shattered_kingdom.characters.players.rogue import Rogue
from the_shattered_kingdom.characters.players.warrior import Warrior


def start() -> None:
    """Start the game and introduce the player's chosen hero."""

    print("Welcome to The Shattered Kingdom!", end="\n\n")

    hero = create_hero()
    hero.introduce()


def create_hero() -> Character:
    """Prompt the player to create a hero and choose a character class."""

    hero_name = input("Enter your hero's name: ")

    if not hero_name.isalpha():
        raise ValueError("Hero name must only contain characters.")

    while True:
        print("\nChoose your class: ")
        print("1: Warrior")
        print("2: Mage")
        print("3: Rogue")

        try:
            class_choice = int(input())
        except ValueError:
            print("Please enter a number from 1 to 3.")
            continue

        match class_choice:

            case 1:
                return Warrior(hero_name)

            case 2:
                return Mage(hero_name)

            case 3:
                return Rogue(hero_name)

            case _:
                print("\nInvalid choice, selection must be a number from 1 to 3.")
                continue


if __name__ == "__main__":
    start()