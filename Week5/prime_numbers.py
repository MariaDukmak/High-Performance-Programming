import time
import numpy as np

# def priemgetal(maximum):
#     priem, count, k = [], 0, 2 # array met alle priemgetallen vanaf 2 t/m een maximum
#
#     for i in range(k, maximum):
#         priem.append(i)
#
#     # Loop door de lijst
#     for j in priem:
#         count += 1
#         for i in priem:
#             if i % j == 0:
#                 if i != j:priem.remove(i)
#     return priem, count

def sequentiele_zeef (N, return_primes=False):
    k = 2
    sieve = np.full(N, True, dtype=bool)
    root_N = int(N**0.5)
    for (i,), (is_prime) in np.ndenumerate(sieve[k:root_N+1]):
    # for (i,), (_) in np.ndenumerate(sieve[k:root_N+1]):
        k = i + 2
        # if is_prime:
        #     print(is_prime)
        # print("i",i)
        # print(k)
        # print("hier",sieve[k*2::k])
        sieve[k*2::k] = False
    sieve[0:2] = False

    # if return_primes:
    #     return np.arange(N)[sieve]
    # else:
    return np.sum(sieve)


def test_priemgetal():
    """
    Een functie die de werking van de priemgetal tot en met 20 test.
    """
    assert len(sequentiele_zeef (20)) == len([2, 3, 5, 7, 11, 13, 17, 19]), "De priemgetallen zijn niet hetzelfde"


if __name__ == "__main__":

    start_time = time.time()
    priemgetallen = sequentiele_zeef(1000000000)
    total_time = time.time() - start_time

    # print(f"Totaal: {count}")
    print(f"Lijst van alle priemgetallen: {priemgetallen}")
    print(f"Sequential algorithm took: {total_time:.5f} second(s)")

    # Check of het algoritme goed werkt
    # test_priemgetal()
