from Week2.Inlever_opdracht.mulriprocesse_merge_sort import generate_list, merge_sort_parallel
from Week2.Inlever_opdracht.threaded_merge _sort import merge_sort_parallel_thread

import unittest


class Test(unittest.TestCase):
    def test_multiprocess(self):
        lijst = generate_list(1000)
        for i in [1,2,4,8]:
            self.assertEqual(sorted(lijst), merge_sort_parallel(lijst, i))

    def test_multithreading(self):
        lijst = generate_list(1000)
        for i in [1,2,4,8]:
            self.assertEqual(sorted(lijst), merge_sort_parallel_thread(lijst, i))

if __name__ == '__main__':
    unittest.main()