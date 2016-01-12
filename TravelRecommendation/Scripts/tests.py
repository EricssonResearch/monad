class TestStringMethods(unittest.TestCase):
    tr = TravelRecommendation()
    tr.dataBaseConnection()
    tr.populateFromDatabase()

    def test1_dataBaseConnection(self):
        self.assertEqual(str(self.tr.client), "MongoClient('localhost', 27017)")
        self.assertEqual(str(self.tr.db), "Database(MongoClient('localhost', 27017), u'monad')")
        print "\nTest 1 - Connected to Database successfully"

    def test2_populateFromDatabase(self):
        self.assertTrue(len(self.tr.users) != 0)
        self.assertTrue(len(self.tr.routes) != 0)
        print "\nTest 2 - Database populated successfully"

    def test3_toSeconds(self):
        a = datetime.datetime(2015,1,1,0,0,1)
        b = datetime.datetime(2000,2,3,23,59,59)
        self.assertTrue(self.tr.toSeconds(a), 1)
        self.assertTrue(self.tr.toSeconds(b), 86399)
        print "\nTest 3 - Datetime conversion to seconds done successfully"

    def test4_toCoordinates(self):
        a = 0
        b = 21600
        c = 43200
        d = 86400
        self.assertTrue(self.tr.toCoordinates(a), (13750, 0))
        self.assertTrue(self.tr.toCoordinates(b), (0, 13750))
        self.assertTrue(self.tr.toCoordinates(c), (-13750, 0))
        self.assertTrue(self.tr.toCoordinates(d), (0, -13750))
        print "\nTest 4 - Seconds conversion to coordinates done successfully"

    def test5_timeNormalizer(self):
        a = 13750
        b = -12345
        c = 83000
        self.assertTrue(self.tr.toCoordinates(a), 0.5)
        self.assertTrue(self.tr.toCoordinates(b), 0.025545454545454545)
        self.assertTrue(self.tr.toCoordinates(c), 1.759090909090909)
        print "\nTest 5 - Time normalization done successfully"

    def test6_latNormalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(self.tr.latNormalizer(a), 0.5089428571428637)
        self.assertTrue(self.tr.latNormalizer(b), 0.4316214285714063)
        self.assertTrue(self.tr.latNormalizer(c), -426.9999999999983)
        print "\nTest 6 - Latitude normalization done successfully"

    def test7_lonNormalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(self.tr.latNormalizer(a), 192.36932727272827)
        self.assertTrue(self.tr.latNormalizer(b), 192.3201227272737)
        self.assertTrue(self.tr.latNormalizer(c), -79.6818181818186)
        print "\nTest 7 - Longitude normalization done successfully"
