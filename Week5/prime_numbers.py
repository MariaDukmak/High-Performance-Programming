import time
import numpy as np


def sequentiele_zeef(N):
    """
    In deze functie wordt een sequentiele implemntatie van de zeef gemaakt.
    We maken gebruik van de functie .remove() hier. Dit zou erg oneffecient
    moeten zijn.

    K: we zitten K op 2, omdat 1 geen priem getal is

    Return:
    ------
    priem: List
        een lijst met de gevonden priem getallen
    count: Int
        een int met de anataal gevonden priem getallen
    """
    count, k = 0, 2
    zeef = [i for i in range(k, N)]
    # Loop door de lijst
    for j in zeef:
        count += 1
        for i in zeef:
            if i % j == 0:
                if i != j: zeef.remove(i)
    return zeef, count


def sequentiele_zeef_vector(N):
    """
    Een betere versie van de zeef. Hier maak ik gebruik van de wortel van
    N om de max aantaal prim getallen te vinden. Deze functie werkt efficienter
    dan de andere functie

    Return:
    ------
    Sum of sieve:
            De sum van de zeef/aantaal gevonden priemgetallen
    """
    k = 2
    zeef = np.full(N, True, dtype=bool)
    root_N = int(N**0.5)
    for i in range(len(zeef[k:root_N+1])):
        k = i + 2
        zeef[k*2::k] = False
    zeef[0:2] = False

    return np.sum(zeef)


def test_priemgetal():
    """
    Een functie die de werking van de priemgetal tot en met 20 test.
           Deze functie test alleen de sequentiele zeef
    """
    assert sequentiele_zeef(20)[0] == [2, 3, 5, 7, 11, 13, 17, 19], "De priemgetallen zijn niet hetzelfde"


if __name__ == "__main__":

    start_time = time.time()
    priemgetallen = sequentiele_zeef_vector(10)
    total_time = time.time() - start_time

    print(f"Lijst van alle priemgetallen: {priemgetallen}")
    print(f"Sequential algorithm took: {total_time:.4f} second(s)")

    # Check of het algoritme goed werkt
    test_priemgetal()

    # Run de normale zeef
    start_time = time.time()
    priemgetallen, count = sequentiele_zeef(10)
    total_time = time.time() - start_time

    print(f"Totaal: {count}")
    print(f"Lijst van alle priemgetallen: {priemgetallen}")
    print(f"Sequential algorithm took: {total_time:.4f} second(s)")
