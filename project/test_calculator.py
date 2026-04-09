# test_calculator.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        self.assertEqual(calc.add(2, 5), 5)
        self.assertEqual(calc.add(-1, 0), 0)
        self.assertEqual(calc.add(0, 0), 0)

if __name__ == '__main__':
    unittest.main()