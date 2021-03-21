
# Using MPI

from mpi4py import MPI
import time

start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_num = (rank * 2) + 1
maximum = 1000

priem = [] # list with all the prime numbers

# Loop through the numbers
for i in range(start_num, maximum, size * 2):
    true_prime = True
    for div_number in range(2, i):
        if i % div_number == 0:
            true_prime = False
            break
    if true_prime:
        priem.append(i)

results = comm.gather(priem, root=0)

# The master worker
if rank == 0:
    total_time = time.time() - start_time
    print(f"Algorithm took: {total_time:.5f} second(s)")