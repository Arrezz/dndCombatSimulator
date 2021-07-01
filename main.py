import random


class Combatant:
    health = 0
    ac = 0
    toHit = 0
    damage = 0
    damageDie = 0
    initiative = 0
    initiativeDie = 0

    name = ""

    def __init__(self, health, ac, toHit, damage, damageDie, initiative, initiativeDie, name):
        self.health = health
        self.ac = ac
        self.toHit = toHit
        self.damage = damage
        self.initiative = initiative
        self.name = name
        self.damageDie = damageDie
        self.initiativeDie = initiativeDie


def dXroll(upperbound):
    return random.randint(1, upperbound)


def fight(fighterperson, monsterperson):
    initFighter = dXroll(fighterperson.initiativeDie) + fighterperson.initiative
    initMonster = dXroll(fighterperson.initiativeDie) + monsterperson.initiative
    turnCounter = 0

    print("Here are our contestants:")
    print("")
    print("Name: " + fighterperson.name)
    print("Health: " + fighterperson.health.__str__())
    print("To hit bonus: " + fighterperson.toHit.__str__())
    print("Damage bonus: " + fighterperson.damage.__str__())
    print("Armor class: " + fighterperson.ac.__str__())
    print("Initiative bonus: " + fighterperson.initiative.__str__())
    print("")
    print("")
    print("Name: " + monsterperson.name)
    print("Health: " + monsterperson.health.__str__())
    print("To hit bonus: " + monsterperson.toHit.__str__())
    print("Damage bonus: " + monsterperson.damage.__str__())
    print("Armor class: " + monsterperson.ac.__str__())
    print("Initiative bonus: " + monsterperson.initiative.__str__())
    print("")
    print("")

    while fighterperson.health > 0 and monsterperson.health > 0:
        turnCounter += 1
        if initFighter >= initMonster:
            damageRoll = dXroll(fighterperson.damageDie) + fighterperson.damage
            print("The " + fighterperson.name + " deals " + damageRoll.__str__())
            monsterperson.health -= damageRoll
            if monsterperson.health < 0:
                monsterperson.health = 0
            print(monsterperson.health.__str__() + " health left for " + monsterperson.name)
            initFighter -= 20
        else:
            damageRoll = dXroll(monsterperson.damageDie) + monsterperson.damage
            print("The " + monsterperson.name + " deals " + damageRoll.__str__())
            fighterperson.health -= damageRoll
            if fighterperson.health < 0:
                fighterperson.health = 0
            print(fighterperson.health.__str__() + " health left for " + fighterperson.name)
            initMonster -= 20
    print("The fight took " + turnCounter.__floor__().__str__() + " turns")
    if fighterperson.health > 0:
        print(fighterperson.name + " won")
        return 0
    else:
        print(monsterperson.name + " won")
        return 1


def inputCustomCombatant():
    fighterHealth = int(input("What do you want the fighters health to be?"))
    fighterAc = int(input("What do you want the fighters ac to be?"))
    fighterToHit = int(input("What do you want the fighters to hit bonus to be?"))
    fighterDamage = int(input("What do you want the fighters damage bonus to be?"))
    fighterDamageDie = int(input("What do you want the fighters damage die size to be? i.e 20 for a d20"))
    fighterInitiative = int(input("What do you want the fighters initiative bonus to be?"))
    fighterInitiativeDie = int(input("What do you want the fighters initiative die to be"))
    fighterName = (input("What do you want the fighters name to be?"))

    monsterHealth = int(input("What do you want the monsters health to be?"))
    monsterAc = int(input("What do you want the monsters ac to be?"))
    monsterToHit = int(input("What do you want the monsters to hit bonus to be?"))
    monsterDamage = int(input("What do you want the monsters damage bonus to be?"))
    monsterDamageDie = int(input("What do you want the monsters damage die size to be? i.e 20 for a d20"))
    monsterInitiative = int(input("What do you want the monsters initiative bonus to be?"))
    monsterInitiativeDie = int(input("What do you want the monsters initiative die to be"))
    monsterName = (input("What do you want the monsters name to be?"))

    fighterperson = Combatant(fighterHealth, fighterAc, fighterToHit, fighterDamage, fighterDamageDie,
                              fighterInitiative, fighterInitiativeDie, fighterName)
    monsterperson = Combatant(monsterHealth, monsterAc, monsterToHit, monsterDamage, monsterDamageDie,
                              monsterInitiative, monsterInitiativeDie, monsterName)

    return fighterperson, monsterperson


if __name__ == '__main__':
    # Inputs
    defaultChoice = input("Do you wish to specify your [C]ombatants or go with [D]efault values? ")
    simulationTrials = int(input("How many times do you want to simulate the combat? (Integer) "))
    roundingPrecisionPercentage = int(input("How many places do you wish to round percentage stats to? (Integer) "))

    # Variables
    fighterWins = 0
    monsterWins = 0
    if roundingPrecisionPercentage == "":
        roundingPrecisionPercentage = 2

    # Code
    if defaultChoice == "C" or defaultChoice == "c":
        defaultFighter = Combatant(20, 16, 4, 3, 6, 0, 20, "fighterperson")
        defaultMonster = Combatant(20, 10, 3, 3, 6, 0, 20, "monsterperson")

        for i in range(0, simulationTrials):
            print("")
            print("Start round " + i.__str__() + "!")
            fighter = defaultFighter
            monster = defaultMonster
            result = fight(fighter, monster)
            if result == 0:
                fighterWins += 1
            else:
                monsterWins += 1

    if defaultChoice == "D" or defaultChoice == "d":
        defaultFighter = Combatant(20, 16, 4, 3, 6, 0, 20, "fighterperson")  # TODO not working currently
        defaultMonster = Combatant(20, 10, 3, 3, 6, 0, 20, "monsterperson")

        for i in range(0, simulationTrials):
            print("")
            print("Start round " + i.__str__() + "!")
            fighter = Combatant(20, 16, 4, 3, 6, 0, 20, "fighterperson")  # TODO not working currently
            monster = Combatant(20, 10, 3, 3, 6, 0, 20, "monsterperson")
            result = fight(fighter, monster)
            if result == 0:
                fighterWins += 1
            else:
                monsterWins += 1

    else:
        print("choice not recognized")
    print("")
    print("Here are the simulation stats:")
    print("")
    print("Monster stats")
    print("Monster wins: " + str(monsterWins))
    print("Monster win percentage: " + str(
        round(((monsterWins / simulationTrials) * 100), roundingPrecisionPercentage)) + "%")
    print("")
    print("Fighter stats")
    print("Fighter wins: " + str(fighterWins))
    print("Fighter win percentage: " + str(
        round(((fighterWins / simulationTrials) * 100), roundingPrecisionPercentage)) + "%")
