"""Copyright 2015 Ericsson AB

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

import inits

def main():
    unittest.main()

class InitTesting(unittest.TestCase):
    """
    Class for testing the init using unittest.
    """

    # Test initRepeatBound
    def testCreating(self):
        self.assertEqual(inits.initRepeatBound(list,lambda: 1, [1,1]),[1])

    # Test that the length of the generated list has a length less or equal
    # to the upper bound.
    def testRandomLength(self):
        l = inits.initRepeatBound(list, lambda: 1, [1,10])
        self.assertLessEqual(len(l), 10)

if __name__ == '__main__':
    main()
