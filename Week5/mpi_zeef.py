from mpi4py import MPI
import time
from sys import argv
import numpy as np
from multiprocessing import Process, Manager, Pool
#
# start_time = time.time()
#
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()
#
# num = (rank * 2) + 1
# maximum, priem = 1000000, []
#
#
# for i in range(num, maximum, size * 2):
#     true_prime = True
#     for div_number in range(2, i):
#         if i % div_number == 0:
#             true_prime = False
#             break
#     if true_prime:
#         priem.append(i)
#
# results = comm.gather(priem, root=0)
#
# # de master worker
# if rank == 0:
#     total_time = round(time.time() - start_time)
#
#     print('Found prime numbers up to: ' + str(maximum))
#     print('Total processes: ' + str(size))
#     print("Algorithm took: {:.5f} second(s)".format(total_time))
#
#     totalPrimes = comm.reduce(results, op=MPI.SUM, root=0)
#     print("The final result", totalPrimes)

def zeef():
    pass


if __name__ == "__main__":
    n = int(argv[1])
    process_num = int(argv[2])
    root_n = int(n**0.5)
    zeef = [i for i in range(2,n)]

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        start = time.time()

    wl = np.array_split(zeef, size)[rank]

    wl_b = np.array_split(wl, process_num)

    thread_pool = Pool(processes=process_num)
    lijst = thread_pool.map(zeef, wl_b)

    totalPrimes = comm.reduce(lijst, op=MPI.SUM, root=0)

    if rank == 0:
        print("Number of primes:", totalPrimes)
        print("Total time: ", time.time() - start)