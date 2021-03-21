import time
from sys import argv
import numpy as np
from mpi4py import MPI
import concurrent.futures
from multiprocessing import Pool

def zeef_vector(N):
    k = 2
    zeef = np.full(N, True, dtype=bool)
    root_N = int(N**0.5)
    for i in range(len(zeef[k:root_N+1])):
        k = i + 2
        zeef[k*2::k] = False
    zeef[0:2] = False

    return np.sum(zeef)

def worker_zeef(N):
    lijst =N[0]
    k = N[1]
    start = N[2]
    index = N[3]
    div_nummber = start + index+k
    if div_nummber % k == 0:
        lijst[index] = False
    else:
        lijst[index] = True

def zeef(N):
    lijst = N[0]
    k= N[1]
    end = N[2]
    for x in range(k*2, end+1, k):
        lijst[x] = False


if __name__ == "__main__":
    start_time = time.time()
    N = int(argv[1])
    process_in_computer = int(argv[2])

    # MPI Variables
    comm = MPI.COMM_WORLD  # communicator object
    rank = comm.Get_rank()  # return rank of this process in a communicator **id**
    size = comm.Get_size()  # return number of processes in a communicator **numprocesses**
    # print(f'Process {rank} out of {size}')

    k=2
    end = (rank*N) + N
    start = (N//size) * rank
    N_root = end**0.5

    # processen = []
    if rank == 0:
        # start_time = time.time() # start time tracking
        N_list = np.full((N//size)+1, True, dtype=bool)
        N_list[0:2] = False

        list_data = [(N_list, i, end) for i in range(k, int(N_root))]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(zeef, N_list)

    else:
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
