import random
from typing import List
import math


def generate_list(size: int = 8):
    return [(random.randint(0, 20)) for _ in range(size)]


def merge_sort(lijst:List[int]):
    if len(lijst) <= 1:
        return lijst

    middel = int(len(lijst)/2)
    print(middel)
    left = merge_sort(lijst[:middel])
    right = merge_sort(lijst[middel:])
    return merge(left, right)


def merge(left, right):
    new_lijst = []

    left, right = left, right

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


