import time

def priemgetal(maximum):
    priem, count, k = [], 0, 2 # array met alle priemgetallen vanaf 2 t/m een maximum

    for i in range(k, maximum):
        priem.append(i)

    # Loop door de lijst
    for j in priem:
        count += 1
        for i in priem:
            if i % j == 0:
                if i != j:priem.remove(i)
    return priem, count


def test_priemgetal():
    """
    Een functie die de werking van de priemgetal tot en met 20 test.
    """
    assert priemgetal(20)[0] == [2, 3, 5, 7, 11, 13, 17, 19], "De priemgetallen zijn niet hetzelfde"


if __name__ == "__main__":

    start_time = time.time()
    priemgetallen, count = priemgetal(1000)
    total_time = time.time() - start_time

    print(f"Totaal: {count}")
    print(f"Lijst van alle priemgetallen: {priemgetallen}")
    print(f"Sequential algorithm took: {total_time:.5f} second(s)")

    # Check of het algoritme goed werkt
    test_priemgetal()
