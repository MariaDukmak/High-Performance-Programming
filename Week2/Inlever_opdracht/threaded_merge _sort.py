import random, statistics, time, concurrent.futures
import seaborn as sns, matplotlib.pyplot as plt
from typing import List


def generate_list(size: int = 8) -> list:
    """
    Een functie die een lijst genereerd van 8 getallen.
    Return:
    ------
    Een lijst van 8 getallen
    """
    return [(random.randint(0, 100)) for _ in range(size)]


def merge(*args):
    """
    Een functie die de merge  van sublijsten doet
    Return:
    ------
    new_lijst: List
        Een gesorteerde sublijst
    """
    new_lijst = []
    left, right = args[0] if len(args) == 1 else args
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            new_lijst.append(left[left_index])
            left_index += 1
        else:
            new_lijst.append(right[right_index])
            right_index += 1
    if left_index == len(left):
        new_lijst.extend(right[right_index:])
    else:
        new_lijst.extend(left[left_index:])

    return new_lijst


def merge_sort(lijst: List[int]):
    """
    Een implementatie van de merge sort algoritme.
    Dit werkt zoals in de notebook uitegelged is

    Return:
    ------
        Een recursive aanroep voor de functie merge
    """
    if len(lijst) <= 1:
        return lijst

    middel = int(len(lijst)/2)
    left = merge_sort(lijst[:middel])
    right = merge_sort(lijst[middel:])
    return merge(left, right)


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


def merge_sort_parallel(lijst: List[int], threads: int):
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
            print(lijst)
        return lijst


def get_time(lijst: List[int], threads: List[int]):
    """
    Een functie die de runtime voor de processen berekent.

    Return:
    ------
    duration: List
        Een lijst met runtimes van alle processen
    """
    duration = []
    for thread in threads:
        start = time.time()
        merge_sort_parallel(lijst, thread)
        end = time.time()

        duration.append(end - start)
        print(f'Parallel Merge Sort with {thread} process(es) took {duration[-1]:.5f} second(s)')
    return duration


def plot_grafiek(times: List[float], threads: List[int]):
    """
    Een functie die een plot maakt van de runtime per process.
    Er wordt ook een bereking gemaakt voor het gemiddelde en de std van de runtimes.

    Return:
    ------
    Een scatterplot
    """

    sns.scatterplot(threads, times)
    plt.xlabel("number of process(es)")
    plt.ylabel("time in second(s)")
    plt.title("Runtime merge sort using multithreading")
    plt.show()
    print(f'Parallel Merge Sort with {len(threads)} workers has average runtime {statistics.mean(times):.5f} second(s) '
          f'and a std of {statistics.stdev(times):5f} second(s)')


if __name__ == "__main__":
    threads = [1, 2, 4, 8]
    random_list = generate_list(50000)
    results = get_time(random_list, threads=threads)

    plot_grafiek(results, threads)


