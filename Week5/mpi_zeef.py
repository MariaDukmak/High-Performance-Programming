from mpi4py import MPI
import time

start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

num = (rank * 2) + 1
maximum, priem = 1000000, []


for i in range(num, maximum, size * 2):
    true_prime = True
    for div_number in range(2, i):
        if i % div_number == 0:
            true_prime = False
            break
    if true_prime:
        priem.append(i)

results = comm.gather(priem, root=0)

# de master worker
if rank == 0:
    total_time = round(time.time() - start_time)

    print('Found prime numbers up to: ' + str(maximum))
    print('Total processes: ' + str(size))
    print("Algorithm took: {:.5f} second(s)".format(total_time))

    totalPrimes = comm.reduce(results, op=MPI.SUM, root=0)
    print("The final result", totalPrimes)
