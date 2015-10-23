from planner import TravelPlanner, Mode
import unittest
import datetime

YEAR  = 2015
MONTH = 10
DAY   = 10

TIMEDIFF_10MIN = datetime.timedelta(minutes = 10)
TIMEDIFF_15MIN = datetime.timedelta(minutes = 15)
TIMEDIFF_25MIN = datetime.timedelta(minutes = 25)
TIMEDIFF_30MIN = datetime.timedelta(minutes = 30)
TIMEDIFF_60MIN = datetime.timedelta(minutes = 60)
TIME_1255H = datetime.datetime(YEAR, MONTH, DAY, 12, 55)
TIME_1300H = datetime.datetime(YEAR, MONTH, DAY, 13, 00)
TIME_1305H = datetime.datetime(YEAR, MONTH, DAY, 13, 05)
TIME_1315H = datetime.datetime(YEAR, MONTH, DAY, 13, 15)

class TestTravelPlanner(unittest.TestCase):

    tp = TravelPlanner()

    def test_init(self):
        requestDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'TravelRequest')"
        routeDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), u'Route')"
        timetableDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'timeTable')"
        usertripDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'UserTrip')"

        self.assertEqual(self.tp.fittingRoutes, [])
        self.assertEqual(self.tp.startingWaypoint, [])
        self.assertEqual(self.tp.endingWaypoint, [])

        self.assertEqual(str(self.tp.travelRequest), requestDBString)
        self.assertEqual(str(self.tp.route), routeDBString)
        self.assertEqual(str(self.tp.timeTable), timetableDBString)
        self.assertEqual(str(self.tp.userTrip), usertripDBString)

    def test_findFittingRoutes(self):
        pass

    def test_isBetterTripStartTime(self):
        self.tp.tripTuples = [("trip", TIMEDIFF_30MIN, TIME_1300H, TIME_1315H)]
        self.tp.timeMode = Mode.startTime

        self.tp.timeToArrival = TIMEDIFF_25MIN
        self.assertTrue(self.tp._isBetterTrip(0))

        self.tp.timeToArrival = TIMEDIFF_30MIN
        self.tp.dptTime = TIME_1305H
        self.tp.routeMode = Mode.tripTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.waitTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.dptTime = TIME_1255H
        self.tp.routeMode = Mode.waitTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.tripTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.timeToArrival = TIMEDIFF_60MIN
        self.assertFalse(self.tp._isBetterTrip(0))

    def test_isBetterTripArrivalTime(self):
        self.tp.tripTuples = [("trip", TIMEDIFF_30MIN, TIME_1300H, TIME_1315H)]
        self.tp.timeMode = Mode.arrivalTime

        self.tp.diffToArrTime = TIMEDIFF_25MIN
        self.assertTrue(self.tp._isBetterTrip(0))

        self.tp.diffToArrTime = TIMEDIFF_30MIN
        self.tp.dptTime = TIME_1305H
        self.tp.routeMode = Mode.tripTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.waitTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.dptTime = TIME_1255H
        self.tp.routeMode = Mode.waitTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.tripTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.diffToArrTime = TIMEDIFF_60MIN
        self.assertFalse(self.tp._isBetterTrip(0))

    # The number of tests is very important!
    def test_hereIsOneMoreTestThatWillSucceed(self):
        pass

if __name__ == "__main__":
    unittest.main()

