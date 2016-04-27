import unittest
from tsdb import TreeIndex

class TreeIndexTests(unittest.TestCase):

    def setUp(self):
        self.blarg_index = TreeIndex(database_name='test',fieldName='blarg')
        self.blarg_index.insert(1,'ts-1')
        self.blarg_index.insert(1,'ts-2')
        self.blarg_index.insert(1,'ts-3')
        self.blarg_index.insert(1,'ts-4')
        self.blarg_index.insert(1,'ts-5')
        self.blarg_index.insert(2,'ts-6')
        self.blarg_index.insert(7,'ts-7')
        self.blarg_index.insert(8,'ts-8')
        self.blarg_index.insert(2,'ts-9')
        self.blarg_index.insert(8,'ts-10')

    def tearDown(self):
        self.blarg_index.deleteIndex()

    def test_get(self):
        self.assertEqual(set(self.blarg_index.getEqual(8)),set(['ts-8','ts-10']))

    def test_getHigher(self):
        self.assertEqual(set(self.blarg_index.getHigherThan(6)),set(['ts-7','ts-8','ts-10']))

    def test_getLower(self):
        self.assertEqual(set(self.blarg_index.getLowerThan(2)),set(['ts-1','ts-2','ts-3','ts-4','ts-5']))

    def test_missingField(self):
        self.assertEqual(set(self.blarg_index.getEqual(11)),set([]))

    def test_remove(self):
        self.assertEqual(set(self.blarg_index.getEqual(8)),set(['ts-8','ts-10']))
        self.blarg_index.remove(fieldValue=8,pk='ts-8')
        self.assertEqual(set(self.blarg_index.getEqual(8)),set(['ts-10']))

    def test_missingPK(self):
        with self.assertRaises(ValueError):
            self.blarg_index.remove(fieldValue=8,pk='ts-100')
