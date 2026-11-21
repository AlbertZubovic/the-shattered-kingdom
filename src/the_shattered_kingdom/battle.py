from .characters import Character

class Battle:
    """Represent a class representing the combat and statistics of a battle between two characters."""

    def __init__(self, combatant_a: Character, combatant_b: Character) -> None:
        if not isinstance(combatant_a, Character):
            raise TypeError("Combatant A must be a character.")

        if not combatant_a.is_alive():
            raise ValueError(f"{combatant_a} has already been defeated.")

        if not isinstance(combatant_b, Character):
            raise TypeError("Combatant B must be a character.")

        if not combatant_b.is_alive():
            raise ValueError(f"{combatant_b} has already been defeated.")

        if combatant_a is combatant_b:
            raise ValueError(f"{combatant_a} cannot initiate a battle with itself.")

        self.__combatant_a = combatant_a
        self.__combatant_b = combatant_b

        self.__started = False


    def start_battle(self) -> Character:
        """Initiates a battle loop which runs until a combatant is defeated."""

        if self.__started:
            raise RuntimeError("This battle has already commenced.")

        self.__started = True

        print(f"Battle between {self.__combatant_a} and {self.__combatant_b} is commencing.")
        attacker = self.__combatant_a
        defender = self.__combatant_b

        while True:
            print("-------------------------------------------------------")

            a_alive = self.__combatant_a.is_alive()
            b_alive = self.__combatant_b.is_alive()

            if not (a_alive and b_alive):
                winner = self.__combatant_a if a_alive else self.__combatant_b
                loser = self.__combatant_b if a_alive else self.__combatant_a

                print(f"{winner.name} has won the battle against {loser.name}.")
                return winner

            attacker.attack_target(defender)
            attacker, defender = defender, attacker




