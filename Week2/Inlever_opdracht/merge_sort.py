import random
from typing import List
import time
import multiprocessing
import seaborn as sns
import matplotlib.pyplot as plt


def generate_list(size: int = 8):
    return [(random.randint(0, 100)) for _ in range(size)]


def merge_sort(lijst: List[int]):
    if len(lijst) <= 1:
        return lijst

    middel = int(len(lijst)/2)
    left = merge_sort(lijst[:middel])
    right = merge_sort(lijst[middel:])
    return merge(left, right)


def merge(*args):
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


def split_for_multiprocess(lijst: List[float], process: int):
    split = int(round(float(len(lijst)) / process))
    split_list = []
    for i in range(process):
        sub_list = lijst[i * split:(i + 1) * split]
        split_list.append(sub_list)
    full_list = split_list if split_list else None

    return full_list


def merge_sort_parallel(lijst: List[float], process: int):
    pool = multiprocessing.Pool(processes=process)
    list_splitted = split_for_multiprocess(lijst, process)
    lijst = pool.map(merge_sort, list_splitted)
    # ik weet niet of ik nog verder moet joinen
    lijst = sum(lijst, [])
    # flatten = lambda t: [item for lijst in t for item in lijst]
    # print(list(flatten))


def get_time(lijst: List[float], processes: List[int]):
    duration = []
    for process in processes:
        start = time.time()
        merge_sort_parallel(lijst, process)
        end = time.time()

        duration.append(end - start)
        print(f'Parallel Merge Sort with {process} process(es) took {duration[-1]:.5f} second(s)')
    return duration


def plot_grafiek(times: List[float], processes: List[int]):
    sns.scatterplot(processes, times)
    plt.show()


if __name__ == "__main__":
    processen = [1, 2, 4, 8]
    random_list = generate_list(42069)
    results = get_time(random_list, processes=processen)

    plot_grafiek(results, processen)
