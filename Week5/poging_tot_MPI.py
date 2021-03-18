from mpi4py import MPI
import time
import numpy as np
#
# comm = MPI.COMM_WORLD  # communicator object
# rank = comm.Get_rank()  # return rank of this process in a communicator    id
# size = comm.Get_size()  # return number of processes in a communicator     numprocesses
start_time = time.time()

comm = MPI.COMM_WORLD  # communicator object
rank = comm.Get_rank()  # return rank of this process in a communicator    id
size = comm.Get_size()  # return number of processes in a communicator     numprocesses

start_num = (rank * 2) + 1
maximum, priem = 1000000, []


for i in range(start_num, maximum, size * 2):
    true_prime = True
    for div_number in range(2, i):
        if i % div_number == 0:
            true_prime = False
            break
    if true_prime:
        priem.append(i)


results = comm.gather(priem, root=0)

if rank == 0:
    total_time = round(time.time() - start_time)

    print('Found prime numbers up to: ' + str(maximum))
    print('Total processes: ' + str(size))
    print("Algorithm took: {:.5f} second(s)".format(total_time))

    # merge de processen van MPI
    merged_priem = [item for sublist in results for item in sublist]
    merged_priem.sort()
    print('Amount of primes found: ' + str(len(merged_priem)))