# run test in cli or 

import unittest
import take06 as reversi

class TestObjectCreation(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass	

	def test_creation_host(self):
		h = reversi.Brett(4)
		self.assertEqual(h.max_number_stones, 16)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.max_number_stones)

		h = reversi.Brett(5)
		self.assertEqual(h.max_number_stones, 25)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.max_number_stones)

		h = reversi.Brett(10)
		self.assertEqual(h.max_number_stones, 100)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.max_number_stones)

	def test_creation_board(self):
		pass

	def test_creation_player(self):
		pass	


if __name__ == '__main__':
	unittest.main()