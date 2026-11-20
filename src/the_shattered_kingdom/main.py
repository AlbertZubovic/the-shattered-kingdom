from characters import Character

def main() -> None:
    arin = Character("Arin", 100, 10, 5)
    quake = Character("Quake", 150, 25, 15)

    print(arin)
    print(quake)

    arin.take_damage(20)

    print(arin)

    arin.heal(15)

    print(arin)

    arin.take_damage(150)

    print(arin)

    print(arin.is_alive())


if __name__ == "__main__":
    main()