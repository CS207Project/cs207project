import unittest
from tsdb import BitmapIndex
import os

class BitmapIndexTests(unittest.TestCase):

    def setUp(self):
        self.dirPath = "files/testing"
        if not os.path.isdir(self.dirPath):
            os.makedirs(self.dirPath)
            self._createdDirs = True
        else:
            self._createdDirs = False

        self.space_index = BitmapIndex(values = ['comet','alien','satellite'], pk_len=4,\
                            database_name='testing',fieldName='outerspace')
        self.space_index.insert('comet','ts-1')
        self.space_index.insert('comet','ts-2')
        self.space_index.insert('comet','ts-3')
        self.space_index.insert('alien','ts-4')
        self.space_index.insert('alien','ts-5')
        self.space_index.insert('satellite','ts-6')


    def tearDown(self):
        self.space_index.deleteIndex()
        if self._createdDirs:
            os.removedirs(self.dirPath)

    def test_getEqual(self):
        self.assertEqual(set(self.space_index.getEqual('alien')),set(['ts-4','ts-5'])))

    def test_getNotEq(self):
        self.assertEqual(set(self.space_index.getNotEq('comet')),set(['ts-4','ts-5','ts-6']))

    def test_wrongLengthKey(self):
        with self.assertRaises(ValueError):
            self.space_index.insert('alien','ts-4000000')

    def test_fakeField(self):
        with self.assertRaises(ValueError):
            self.space_index.insert('moon','ts-1')

    def test_update(self):
        self.space_index.insert('alien','ts-1')
        self.assertEqual(set(self.space_index.getEqual('alien')), set(['ts-1', 'ts-4','ts-5']))

    def test_get(self):
        self.assertEqual(set(self.space_index.get('ts-6')), set('satellite'))

    def test_remove(self):
        self.space_index.remove('ts-1')
        self.assertEqual(set(self.space_index.getEqual('alien')), set(['ts-4', 'ts-5']))

    def test_allKeys_andInsertNew(self):
        self.insert('satellite','ts-7')
        self.assertEqual(set(self.space_index.allKeys()), set(['ts-2', 'ts-3', 'ts-4', 'ts-5', 'ts-6', 'ts-7']))

if __name__ == '__main__':
    unittest.main()
