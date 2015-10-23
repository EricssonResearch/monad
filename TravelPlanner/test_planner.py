from planner import TravelPlanner, Mode
import unittest


class TestTravelPlanner(unittest.TestCase):

    tp = TravelPlanner()
    requestDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
            "u'TravelRequest')"
    routeDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), u'Route')"
    timetableDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
            "u'timeTable')"
    usertripDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
            "u'UserTrip')"

    def test_init(self):
        self.assertEqual(self.tp.fittingRoutes, [])
        self.assertEqual(self.tp.startingWaypoint, [])
        self.assertEqual(self.tp.endingWaypoint, [])

        self.assertEqual(str(self.tp.travelRequest), self.requestDBString)
        self.assertEqual(str(self.tp.route), self.routeDBString)
        self.assertEqual(str(self.tp.timeTable), self.timetableDBString)
        self.assertEqual(str(self.tp.userTrip), self.usertripDBString)

    def test_findFittingRoutes(self):
        pass

    def test_isBetterTrip(self):
        pass


if __name__ == "__main__":
    unittest.main()
