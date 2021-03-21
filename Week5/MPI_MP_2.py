import time
from sys import argv
import numpy as np
from mpi4py import MPI
import concurrent.futures
from multiprocessing import Pool


def worker_zeef(N):
    lijst, k, start, index = N[0], N[1], N[2], N[3]
    if (start + k + index) % k == 0:
        lijst[index] = False
    else: lijst[index] = True

def zeef(N):
    lijst, k, end = N[0], N[1], N[2]
    for x in range(k*2, end+1, k):
        lijst[x] = False


if __name__ == "__main__":
    N, process_in_computer = int(argv[1]), int(argv[2])

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    k=2
    end = (rank*N) + N
    N_root = end**0.5
    start = (N//size) * rank

    # processen = []
    if rank == 0:
        start_time = time.time()
        N_list = np.full((N//size)+1, True, dtype=bool)
        N_list[0:2] = False

        list_data = [(N_list, i, end) for i in range(k, int(N_root))]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(zeef, N_list)

    N_list = np.full((N//size), True, dtype=bool)

    while k**2 <= end:
        if k <(start) or (N_list[k]):
            list_data = [(N_list, k, start, i) for i in range(k, (N//size))]
            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(worker_zeef, N_list)
        k += 1

    result = np.sum(N_list)
    resultresult = comm.reduce(result, op =MPI.SUM, root=0)

    if rank == 0:
        print("Number of primes:", resultresult)
        print("Total time: ", time.time() - start_time)
