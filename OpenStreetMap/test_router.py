"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import unittest
import os.path

import router

FILE = "testmap.xml"


def main():
    unittest.main()


class RouterTester(unittest.TestCase):
    """
    Class for testing the router.py
    """

    @classmethod
    def setUpClass(cls):
        if os.path.isfile(FILE):
            cls._map = router.Map(FILE)
            cls._map.parsData()
        else:
            assert False, ("File not found: ", FILE)

    # set up the test
    def setUp(self):
        pass

    @unittest.skipUnless(os.path.isfile(FILE), "fileNotFound")
    def testPathFinder(self):
        self.assertGreater(len(self._map.findRoute(-439079, -439083)), 0)

        # The path from one node to itself should be itself.
        self.assertEqual(self._map.findRoute(-439079, -439079), [-439079])

    @unittest.skipUnless(os.path.isfile(FILE), "fileNotFound")
    def test(self):
        pass

if __name__ == '__main__':
    main()
