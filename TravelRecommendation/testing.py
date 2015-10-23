import unittest
import datetime
import TravelRecommendation as tr
from geopy.distance import vincenty

class TestStringMethods(unittest.TestCase):

    req, tt = tr.dataBaseConnection()
    tr.populateFromDatabase(req, tt)

    def test1_dataBaseConnection(self):
        self.assertEqual(str(self.req),
        "Collection(Database(MongoClient('localhost', 27017), u'monad')," \
        " u'TravelRequest')")
        self.assertEqual(str(self.tt),
        "Collection(Database(MongoClient('localhost', 27017), u'monad')," \
        " u'TimeTable')")
        print "\nTest 1 - OK ... Connected to Database"

    def test2_populateFromDatabase(self):
        self.assertEqual(str(type(self.req.find())),
        "<class 'pymongo.cursor.Cursor'>")
        self.assertEqual(str(type(self.req.find())),
        "<class 'pymongo.cursor.Cursor'>")
        print "\nTest 2 - OK ... Database populated"

    def test3_toSeconds(self):
        a = datetime.datetime(2015,1,1,0,0,1)
        b = datetime.datetime(2000,2,3,23,59,59)
        self.assertTrue(tr.toSeconds(a), 1)
        self.assertTrue(tr.toSeconds(b), 86399)
        print "\nTest 3 - OK ... Datetime conversion to seconds"

    def test4_toCoordinates(self):
        a = 0
        b = 21600
        c = 43200
        d = 86400
        self.assertTrue(tr.toCoordinates(a), (13750, 0))
        self.assertTrue(tr.toCoordinates(b), (0, 13750))
        self.assertTrue(tr.toCoordinates(c), (-13750, 0))
        self.assertTrue(tr.toCoordinates(d), (0, -13750))
        print "\nTest 4 - OK ... Seconds conversion to coordinates"

    def test5_timeNormalizer(self):
        a = 13750
        b = -12345
        c = 83000
        self.assertTrue(tr.toCoordinates(a), 0.5)
        self.assertTrue(tr.toCoordinates(b), 0.025545454545454545)
        self.assertTrue(tr.toCoordinates(c), 1.759090909090909)
        print "\nTest 5 - OK ... Time normalization"

    def test6_latNormalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(tr.latNormalizer(a), 0.5089428571428637)
        self.assertTrue(tr.latNormalizer(b), 0.4316214285714063)
        self.assertTrue(tr.latNormalizer(c), -426.9999999999983)
        print "\nTest 6 - OK ... Latitude normalization"

    def test7_lonNormalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(tr.latNormalizer(a), 192.36932727272827)
        self.assertTrue(tr.latNormalizer(b), 192.3201227272737)
        self.assertTrue(tr.latNormalizer(c), -79.6818181818186)
        print "\nTest 7 - OK ... Longitude normalization"

    def test8_calculateDistance(self):
        a = (1,1)
        tr.selected_centroids = [(2,2)]
        self.assertEqual(tr.calculateDistance(a) ,[1.4142135623730951])
        b = (1,2,3)
        tr.selected_centroids = [(2,3,3), (1,1,1)]
        self.assertEqual(tr.calculateDistance(b), [1.4142135623730951,
        2.2360679774997898])
        print "\nTest 8 - OK ... Calculating distance"

    def test9_removeDuplicates(self):
        a = [(1,2), (1,3), (1,4), (2,3)]
        b = [(1,2), (2,2), (3,2)]
        self.assertEqual(tr.removeDuplicates(a), [1,2])
        self.assertEqual(tr.removeDuplicates(b), [1,2,3])
        print "\nTest 9 - OK ... Removing duplicates"

    def test10_timeApproximation(self):
        self.assertEqual(tr.timeApproximation(59.851252, 17.593290,
                                              59.858052, 17.644739), 18)
        self.assertEqual(tr.timeApproximation(59.851252, 17.593290,
                                              59.840427, 17.647628), 20)
        print "\nTest 10 - OK ... Approximating time"

if __name__ == "__main__":
    unittest.main()
