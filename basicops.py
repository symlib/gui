import sys
import unittest
from  create_delete_multi import CreateDeleteMulti

class Test_Suite(unittest.TestCase):
    def test_create_delete_multi_pool_volume_snapshot_clone(self):
        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(CreateDeleteMulti.test_create_delete_multi),
        ])
        runner = unittest.TextTestRunner()
        runner.run(self.suite)


import unittest

if __name__ == "__main__":
    unittest.main()