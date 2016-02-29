import unittest
from binary_search import binary_search as bs

class UnitTests(unittest.TestCase):

    inf = float('inf')
    nan = float('nan')
    input = range(1, 10)

    def invalid_data(self):
        with self.assertRaises(TypeError):
            bs('Invalid Text', 5)

    def array_length(self):
        self.assertEqual(bs([], 1), -1) # length 0
        self.assertEqual(bs([1], 1), 0) # length 1
        self.assertEqual(bs([0, 1], 1), 1) # length 2
        self.assertEqual(bs([0, 1], 1, 0, 0), -1) # value out of [min...max]

    def weird_data(self):
        self.assertEqual(bs([5, 1.5, 10], 1.5), 2) # Float #1
        self.assertEqual(bs([1.5, 5, 10], 5), 1) # Float #2
        self.assertEqual(bs([5, 10, inf], inf), 2) # Infinity
        self.assertEqual(bs([5, nan, 10], nan), 1) # NaN

    def ranges(self):
        self.assertEqual(bs(input, -5), -1) # less than min element
        self.assertEqual(bs(input, 15), -1) # greater than max element
        self.assertEqual(bs(input, 4.5), -1) # between min and max, but not found


if __name__ == '__main__':
    unittest.main()
