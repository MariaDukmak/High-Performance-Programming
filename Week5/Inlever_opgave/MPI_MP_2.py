"""
In de code hieronder maak ik gebruik van MPI en MP om de priem getallen in N te vinden.
"""

import time
from sys import argv
import numpy as np
from mpi4py import MPI
import concurrent.futures


def zeef_vector(N):
    """
    Deze functie vindt de priem getallen van een lijst door gebruik van Numpy te maken.
    N: len van de lijst
    """
    k = 2
    zeef = np.full(N, True, dtype=bool)
    root_N = int(N**0.5)
    for i in range(len(zeef[k:root_N+1])):
        k = i + 2
        zeef[k*2::k] = False
    zeef[0:2] = False

    return np.sum(zeef)


def worker_zeef(N):
    """
    Een functie die de prime getallen per sublist van de workers berekent.
    Hier wordt gebruik van de lijst, k, de start waarde en de index gemaakt.
    return: Nothing
    """
    N_lijst =N[0]
    k = N[1]
    start = N[2]
    index = N[3]
    div_nummber = start + index+k
    if div_nummber % k == 0:
        N_lijst[index] = False
    else:
        N_lijst[index] = True


def zeef(N):
    """
    Een functie die de primes voor de masterworker berekent
    """
    N_lijst = N[0]
    k= N[1]
    end = N[2]
    for x in range(k*2, end+1, k):
        N_lijst[x] = False


if __name__ == "__main__":
    N = int(argv[1])
    process_in_computer = int(argv[2])

    # MPI Variables
    comm = MPI.COMM_WORLD  # communicator object
    rank = comm.Get_rank()  # return rank of this process in a communicator **id**
    size = comm.Get_size()  # return number of processes in a communicator **numprocesses**
    # print(f'Process {rank} out of {size}')

    # Maak variabelen aan die nodig zijn voor
    # de goed bereken van k, end en de start voor de while loop
    start = (N // size) * rank
    end = (N//size) + start
    N_root = end**0.5
    k=2

    list_data = []

    #Master worker
    if rank == 0:
        start_time = time.time() # start time tracking
        N_list = np.full((N//size)+1, True, dtype=bool)
        N_list[0:2] = False # Zet 0 en 1 al op False

        # Maak een lijst met de subdata
        for i in range(k, int(N_list)):
            list_data.append([N_list, i, end])

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(zeef, list_data)

    else:
        # Maak de True lijst aan
        N_list = np.full((N//size), True, dtype=bool)

        # Bereken de priem nummers met behulp van processen
        while k**2 <= end:
            if k <(start) or (N_list[k]):
                for i in range(k, (N // size)):
                    list_data.append([N_list, k, start, i])

                with concurrent.futures.ProcessPoolExecutor() as executor:
                    executor.map(worker_zeef, list_data)
            k += 1

    # Gather de resultaten van de multiprocessing en de MPI
    result = np.sum(N_list)
    resultresult = comm.reduce(result, op =MPI.SUM, root=0)

    # Als we klaar zijn, print de resultaten uit!
    if rank == 0:
        print("Number of primes:", result)
        print("Total time: ", time.time() - start_time)
