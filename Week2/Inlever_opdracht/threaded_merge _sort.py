import time

from Week2.Inlever_opdracht.mulriprocesse_merge_sort import generate_list, merge, merge_sort
import statistics,  concurrent.futures
import seaborn as sns, matplotlib.pyplot as plt
from typing import List


def split_for_threading(lijst: List[int], threads: int):
    """
    Een functie die de lijst opgesplist in sublijsten op
    basis van het aantal processen.

    Return:
    ------
    full_list: List
        Een lijst met sublijsten
    """
    split = int(round(float(len(lijst)) / threads))
    split_list = []
    for i in range(threads):
        sub_list = lijst[i * split:(i + 1) * split]
        split_list.append(sub_list)
    full_list = split_list if split_list else None
    return full_list


def merge_sort_parallel_thread(lijst: List[int], threads: int):
    """
    Een functie die de pool van de threads aanmaakt en joint.
    De functie split_for_multiprocess aanroept om de lijst naar
    kleiner lijsten op te splitsen zodat het op een goede manier
    wordt verdeeldt door de workers heen.

    Return:
    ------
    lijst: List
        De gesorteerde lijst

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        list_splitted = split_for_threading(lijst, threads)
        lijst = executor.submit(merge_sort, list_splitted)
        lijst = lijst.result()
        while len(lijst) > 1:
            lijst = [(lijst[i], lijst[i + 1]) for i in range(0, len(lijst), 2)]
            lijst = list(executor.map(merge, lijst))
        return lijst


def get_time(lijst: List[int], processes: List[int]):
    """
    Een functie die de runtime voor de processen berekent.

    Return:
    ------
    duration: List
        Een lijst met runtimes van alle processen
    """
    duration = []
    for process in processes:
        start = time.time()
        merge_sort_parallel_thread(lijst, process)
        end = time.time()

        duration.append(end - start)
        print(f'Parallel Merge Sort with {process} process(es) took {duration[-1]:.5f} second(s)')
    return duration


def plot_grafiek(times: List[float], threads: List[int], lenlist):
    """
    Een functie die een plot maakt van de runtime per process.
    Er wordt ook een bereking gemaakt voor het gemiddelde en de std van de runtimes.

    Return:
    ------
    Een scatterplot
    """

    sns.scatterplot(threads, times)
    plt.xlabel("number of thread(es)")
    plt.ylabel("time in second(s)")
    plt.title(f"Runtime merge sort using threads {lenlist}")
    plt.show()
    print(f'Parallel Merge Sort with {len(threads)} workers has average runtime {statistics.mean(times):.5f} second(s) '
          f'and a std of {statistics.stdev(times):5f} second(s)')


if __name__ == "__main__":
    threads = [1, 2, 4, 8]
    random_list = generate_list(100000)
    results = get_time(random_list, threads)

    plot_grafiek(results, threads, len(random_list))


