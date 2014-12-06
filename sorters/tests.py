import time
import unittest
import random
from sorters import Sorters

class SortedTests(unittest.TestCase):
    def setUp(self):
        self.elements = 11000
        self.to_sort = [random.randint(0,999) for _ in range(self.elements)] 

    def test_sorters(self):
        for algorithm in Sorters.ALGORITHMS:
            start = time.time()
            _sorted = getattr(Sorters, algorithm)(self.to_sort[:], self.elements)
            print(algorithm, "took", time.time()-start)
            self.assertEqual(sorted(self.to_sort),
                             _sorted, """Test of {} has failed, data: {}""".format(algorithm, _sorted))


if __name__ == '__main__':
    unittest.main()
