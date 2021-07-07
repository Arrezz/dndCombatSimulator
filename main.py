import json
import math
import random
from enum import Enum
from types import SimpleNamespace


class Combatant:
    health = 0
    maxhealth = 0
    truemaxhealth = 0  # Used for things that drain max hp but reset on long rest
    temphealth = 0
    ac = 0
    toHit = 0
    damage = 0
    damageDie = 0
    initiative = 0
    initiativeDie = 0
    speed = 0
    critrange = 20

    class Size(Enum):
        Tiny = 1
        Small = 2
        Medium = 3
        Large = 4
        Huge = 5
        Gargantuan = 6

    magicalattacks = False
    silveredattacks = False
    adamantiteattacks = False

    # TODO Deal with resistance and immunities?
    # TODO weapon range stuff?
    # TODO deal with whether we need only base stats and derive from that or we take things like toHit straight up
    # TODO reroll die under certain number?

    advantage = False

    feats = []

    strength = 0
    dexterity = 0
    constitution = 0
    intelligence = 0
    wisdom = 0
    charisma = 0

    skillprof = []

    saveprof = []

    barbarianlevel = 0
    bardlevel = 0
    clericlevel = 0
    druidlevel = 0
    fighterlevel = 0
    monklevel = 0
    paladinlevel = 0
    rangerlevel = 0
    roguelevel = 0
    sorcererlevel = 0
    warlocklevel = 0
    wizardlevel = 0
    customclasslevel = 0

    totalLevel = barbarianlevel + bardlevel + clericlevel + druidlevel + fighterlevel + monklevel + paladinlevel \
                 + rangerlevel + roguelevel + sorcererlevel + warlocklevel + wizardlevel + customclasslevel

    monster = False

    name = ""

    def __init__(self, health, ac, toHit, damage, damageDie, initiative, initiativeDie, name, feats, advantage):
        self.health = health
        self.ac = ac
        self.toHit = toHit
        self.damage = damage
        self.initiative = initiative
        self.name = name
        self.damageDie = damageDie
        self.initiativeDie = initiativeDie
        self.feats = feats
        self.advantage = advantage


def toabilityscoremodifier(abilityscore):
    return math.floor((abilityscore - 10) / 2)


def dXroll(upperbound):
    return random.randint(1, upperbound)


def proficiencybonus(combatant):
    if combatant.monster:
        if 0 < combatant.totalLevel < 5:
            return 2
        if combatant.totalLevel < 9:
            return 3
        if combatant.totalLevel < 13:
            return 4
        if combatant.totalLevel < 17:
            return 5
        if combatant.totalLevel < 21:
            return 6
        if combatant.totalLevel < 25:
            return 7
        if combatant.totalLevel < 29:
            return 8
        else:
            return 9
    else:
        if 0 < combatant.totalLevel < 5:
            return 2
        if combatant.totalLevel < 9:
            return 3
        if combatant.totalLevel < 13:
            return 4
        if combatant.totalLevel < 17:
            return 5
        else:
            return 6


def fight(fighterperson, monsterperson):
    initFighter = dXroll(fighterperson.initiativeDie) + fighterperson.initiative
    initMonster = dXroll(fighterperson.initiativeDie) + monsterperson.initiative
    turnCounter = 0

    print("Here are our contestants:")
    print()
    print("Name: " + fighterperson.name)
    print("Health: " + fighterperson.health.__str__())
    print("To hit bonus: " + fighterperson.toHit.__str__())
    print("Damage bonus: " + fighterperson.damage.__str__())
    print("Armor class: " + fighterperson.ac.__str__())
    print("Initiative bonus: " + fighterperson.initiative.__str__())
    print()
    print()
    print("Name: " + monsterperson.name)
    print("Health: " + monsterperson.health.__str__())
    print("To hit bonus: " + monsterperson.toHit.__str__())
    print("Damage bonus: " + monsterperson.damage.__str__())
    print("Armor class: " + monsterperson.ac.__str__())
    print("Initiative bonus: " + monsterperson.initiative.__str__())
    print()
    print()

    while fighterperson.health > 0 and monsterperson.health > 0:
        turnCounter += 1
        if initFighter >= initMonster:
            if fighterperson.feats.count("Elven Accuracy") > 0 and fighterperson.advantage:
                toHitRoll = max(dXroll(20), dXroll(20), dXroll(20))
            elif fighterperson.advantage:
                toHitRoll = max(dXroll(20), dXroll(20))
            else:
                toHitRoll = dXroll(20)
            toHitRollTotal = toHitRoll + fighterperson.toHit
            print("The " + fighterperson.name + " rolled a " + str(toHitRollTotal) + " to hit " + monsterperson.name) #Better/more accurate printout?
            if toHitRollTotal >= monsterperson.ac:
                damageRoll = dXroll(fighterperson.damageDie) + fighterperson.damage
                if toHitRoll == 20:  # TODO add support for crit ranges
                    damageRoll += dXroll(fighterperson.damageDie)
                    print("The " + fighterperson.name + " crit!")
                print("The " + fighterperson.name + " deals " + damageRoll.__str__())
                monsterperson.health -= damageRoll
                if monsterperson.health < 0:
                    monsterperson.health = 0
                print(monsterperson.health.__str__() + " health left for " + monsterperson.name)
            else:
                print("The " + fighterperson.name + " missed!")
            initFighter -= 20
        else:
            if fighterperson.feats.count("Elven Accuracy") > 0 and fighterperson.advantage:
                toHitRoll = max(dXroll(20), dXroll(20), dXroll(20))
            elif fighterperson.advantage:
                toHitRoll = max(dXroll(20), dXroll(20))
            else:
                toHitRoll = dXroll(20)
            toHitRollTotal = toHitRoll + monsterperson.toHit
            print("The " + monsterperson.name + " rolled a " + str(toHitRollTotal) + " to hit " + fighterperson.name) #Better/more accurate printout?
            if toHitRollTotal >= fighterperson.ac:
                damageRoll = dXroll(monsterperson.damageDie) + monsterperson.damage
                if toHitRoll == 20:  # TODO add support for crit ranges
                    damageRoll += dXroll(monsterperson.damageDie)
                    print("The " + monsterperson.name + " crit!")
                print("The " + monsterperson.name + " deals " + damageRoll.__str__())
                fighterperson.health -= damageRoll
                if fighterperson.health < 0:
                    fighterperson.health = 0
                print(fighterperson.health.__str__() + " health left for " + fighterperson.name)
            else:
                print("The " + monsterperson.name + " missed!")
            initMonster -= 20
    print("The fight took " + turnCounter.__floor__().__str__() + " turns")
    if fighterperson.health > 0:
        print(fighterperson.name + " won")
        return 0
    else:
        print(monsterperson.name + " won")
        return 1


def inputCustomCombatant():
    fighterHealth = int(input("What do you want the fighters health to be? "))
    fighterAc = int(input("What do you want the fighters ac to be? "))
    fighterToHit = int(input("What do you want the fighters to hit bonus to be? "))
    fighterDamage = int(input("What do you want the fighters damage bonus to be? "))
    fighterDamageDie = int(input("What do you want the fighters damage die size to be? i.e 20 for a d20 "))
    fighterInitiative = int(input("What do you want the fighters initiative bonus to be? "))
    fighterInitiativeDie = int(input("What do you want the monsters initiative die to be? i.e 20 for a d20 "))
    fighterName = (input("What do you want the fighters name to be ?"))

    monsterHealth = int(input("What do you want the monsters health to be? "))
    monsterAc = int(input("What do you want the monsters ac to be? "))
    monsterToHit = int(input("What do you want the monsters to hit bonus to be? "))
    monsterDamage = int(input("What do you want the monsters damage bonus to be? "))
    monsterDamageDie = int(input("What do you want the monsters damage die size to be? i.e 20 for a d20 "))
    monsterInitiative = int(input("What do you want the monsters initiative bonus to be? "))
    monsterInitiativeDie = int(input("What do you want the monsters initiative die to be? i.e 20 for a d20 "))
    monsterName = (input("What do you want the monsters name to be? "))

    fighterperson = Combatant(fighterHealth, fighterAc, fighterToHit, fighterDamage, fighterDamageDie,
                              fighterInitiative, fighterInitiativeDie, fighterName)
    monsterperson = Combatant(monsterHealth, monsterAc, monsterToHit, monsterDamage, monsterDamageDie,
                              monsterInitiative, monsterInitiativeDie, monsterName)

    return fighterperson, monsterperson


def simulateFight(fighter, monster):
    fighterWins = 0
    monsterWins = 0
    for i in range(0, simulationTrials):
        print("")
        print("Start round " + i.__str__() + "!")
        result = fight(fighter, monster)
        if result == 0:
            fighterWins += 1
        else:
            monsterWins += 1
    return fighterWins, monsterWins


if __name__ == '__main__':
    # Inputs
    defaultChoice = input("Do you wish to specify your [C]ombatants or go with [D]efault values or go with a [T]extfile? ")
    simulationTrials = int(input("How many times do you want to simulate the combat? (Integer) "))
    roundingPrecisionPercentage = int(input("How many places do you wish to round percentage stats to? (Integer) "))

    # Variables
    if roundingPrecisionPercentage == "":
        roundingPrecisionPercentage = 2

    # Code
    if defaultChoice == "C" or defaultChoice == "c":
        fighter, monster = inputCustomCombatant()

        fighterWins, monsterWins = simulateFight(fighter, monster)

    if defaultChoice == "D" or defaultChoice == "d":
        defaultFighter = Combatant(20, 16, 4, 3, 6, 0, 20, "fighterperson")  # TODO not working currently
        defaultMonster = Combatant(20, 10, 3, 3, 6, 0, 20, "monsterperson")

        fighterWins, monsterWins = simulateFight(fighter, monster)

    if defaultChoice == "T" or defaultChoice == "t":

        fileName = input("What is the name of the file you wish to use including file extension? ")

        file = open(fileName, "r")
        data = json.load(file)
        fighter = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

        monster = fighter
        file.close()

        fighterWins, monsterWins = simulateFight(fighter, monster)

    else:
        print("choice not recognized")
    print()
    print("Here are the simulation stats:")
    print()
    print("Monster stats")
    print("Monster wins: " + str(monsterWins))
    print("Monster win percentage: " + str(
        round(((monsterWins / simulationTrials) * 100), roundingPrecisionPercentage)) + "%")
    print()
    print("Fighter stats")
    print("Fighter wins: " + str(fighterWins))
    print("Fighter win percentage: " + str(
        round(((fighterWins / simulationTrials) * 100), roundingPrecisionPercentage)) + "%")
