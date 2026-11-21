from battle import Battle
from characters import Character

def main() -> None:
    arin = Character("Arin", 100, 50, 10)
    quake = Character("Quake", 150, 40, 15)

    print(arin)
    print(quake)

    battle = Battle(arin, quake)
    winner = battle.start_battle()



if __name__ == "__main__":
    main()