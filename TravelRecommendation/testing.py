import unittest
import datetime
import TravelRecommendation_faster as tr
from numpy import array
from bson.objectid import ObjectId
from geopy.distance import vincenty
from pymongo import MongoClient

class TestStringMethods(unittest.TestCase):

    def test_populate_requests(self):
        tr.users = []
        req = tr.retrieve_requests()
        tr.populate_requests(req)
        self.assertGreater(len(tr.users), 0)
        print "Test - OK ... Stored past requests"

    def test_retrieve_requests(self):
        req = tr.retrieve_requests()
        self.assertEqual(str(req), "Collection(Database(MongoClient(" \
        "'130.238.15.114', 27017), u'monad1'), u'TravelRequest')")
        print "Test - OK ... Retrieved past accessed"

    def test_get_today_timetable(self):
        self.assertEqual(str(type(tr.get_today_timetable())),
        "<class 'pymongo.cursor.Cursor'>")
        print "Test - OK ... Timetable accessed"

    def test_populate_timetable(self):
        tr.routes = []
        tr.populate_timetable()
        if tr.get_today_timetable().count() > 0:
            self.assertGreater(len(tr.routes), 0)
        else:
            self.assertEqual(len(tr.routes), 0)
        print "Test - OK ... Timetable stored"

    def test_iterator(self):
        a = [(datetime.datetime(2015, 12, 11, 3, 22, 4), 59.8130431,
        17.6668168, u'Arrheniusplan'),
        (datetime.datetime(2015, 12, 11, 3, 23, 4), 59.813415, 17.659143,
        u'Djursjukhuset'), (datetime.datetime(2015, 12, 11, 3, 24, 4),
        59.8156478, 17.6591888, u'Campus Ultuna'),
        (datetime.datetime(2015, 12, 11, 3, 25, 4), 59.8185469, 17.6584919,
        u'Veterin\xe4rv\xe4gen'), (datetime.datetime(2015, 12, 11, 3, 27, 4),
        59.8270317, 17.6540772, u'Ekudden'),
        (datetime.datetime(2015, 12, 11, 3, 28, 4), 59.8289436, 17.6511594,
        u'Kronparksg\xe5rden'), (datetime.datetime(2015, 12, 11, 3, 29, 4),
        59.8316683, 17.6500192, u'Gustaf Kjellbergs v\xe4g'),
        (datetime.datetime(2015, 12, 11, 3, 31, 4), 59.8341137, 17.6500153,
        u'Emmy Rappes v\xe4g'), (datetime.datetime(2015, 12, 11, 3, 32, 4),
        59.835713, 17.649659, u'Uppsala Folkh\xf6gskola'),
        (datetime.datetime(2015, 12, 11, 3, 34, 4), 59.8386392, 17.6511529,
        u'Lundellska skolan'), (datetime.datetime(2015, 12, 11, 3, 35, 4),
        59.8402173, 17.6476356, u'Polacksbacken'),
        (datetime.datetime(2015, 12, 11, 3, 36, 4), 59.8399598, 17.639664,
        u'Grindstugan'), (datetime.datetime(2015, 12, 11, 3, 38, 4),
        59.8431801, 17.6384828, u'Uppsala Science Park'),
        (datetime.datetime(2015, 12, 11, 3, 39, 4), 59.850088, 17.643244,
        u'Akademiska sjukhuset s\xf6dra'),
        (datetime.datetime(2015, 12, 11, 3, 40, 4), 59.8497475, 17.643572,
        u'Akademiska sjukhuset'), (datetime.datetime(2015, 12, 11, 3, 41, 4),
        59.8524609, 17.6404635, u'Svandammen'),
        (datetime.datetime(2015, 12, 11, 3, 42, 4), 59.8558965, 17.6444067,
        u'B\xe4verns gr\xe4nd'), (datetime.datetime(2015, 12, 11, 3, 43, 4),
        59.8574377, 17.6458977, u'Centralstationen')]

        self.assertEqual(tr.iterator(a), [(0.236022142857145, 0.6218945454545409,
        0.40896343421923104, 0.44295239459832625, u'Arrheniusplan'),
        (0.238678571428556, 0.5870136363636353, 0.40812001002704273,
        0.44364416445906113, u'Djursjukhuset'),
        (0.2546271428571387, 0.5872218181818116, 0.40727357545778864,
        0.4443322476140367, u'Campus Ultuna'),
        (0.2753349999999992, 0.5840540909090949, 0.4064241466263627,
        0.44501663096314165, u'Veterin\xe4rv\xe4gen'),
        (0.3359407142856987, 0.5639872727272691, 0.4047163709212964,
        0.4463742461957367, u'Ekudden'),
        (0.34959714285715, 0.5507245454545474, 0.4038580565612437,
        0.4470474522321898, u'Kronparksg\xe5rden'),
        (0.36905928571425406, 0.5455418181818119, 0.40299681296557566,
        0.4477169067691902, u'Gustaf Kjellbergs v\xe4g'),
        (0.3865264285714416, 0.5455240909090874, 0.4012656037101964,
        0.449044510434701, u'Emmy Rappes v\xe4g'),
        (0.39794999999997865, 0.543904545454542, 0.40039567101021384,
        0.4497026342875515, u'Uppsala Folkh\xf6gskola'),
        (0.4188514285714396, 0.5506949999999958, 0.39864723227667076,
        0.4510074633850332, u'Lundellska skolan'),
        (0.43012357142855484, 0.5347072727272748, 0.3977687595308634,
        0.45165414378759955, u'Polacksbacken'),
        (0.42828428571429433, 0.49847272727272374, 0.3968874734808786,
        0.4522969849859463, u'Grindstugan'),
        (0.45128642857140344, 0.49310363636362675, 0.395116528635283,
        0.453571100888228, u'Uppsala Science Park'),
        (0.5006285714285578, 0.5147454545454487, 0.3942269035559092,
        0.4542023513348327, u'Akademiska sjukhuset s\xf6dra'),
        (0.4981964285714144, 0.5162363636363563, 0.3933345326041903,
        0.4548297140630195, u'Akademiska sjukhuset'),
        (0.5175778571428252, 0.5021068181818119, 0.3924394327695829,
        0.4554531771287061, u'Svandammen'),
        (0.5421178571428472, 0.5200304545454572, 0.39154162109349755,
        0.45607272866205456, u'B\xe4verns gr\xe4nd'),
        (0.5531264285714069, 0.5268077272727204, 0.3906411146689745,
        0.45668835686769677, u'Centralstationen')])
        print "Test - OK ... Iterator testing"

    def test_nearest_stops(self):
        x1 = 59.851252
        x2 = 59.858052
        y1 = 17.59329
        y2 = 17.644739
        dist = 500
        self.assertEqual(tr.nearest_stops(x1,y1,dist),
        ['Reykjaviksgatan', 'Ekebyhus'])
        self.assertEqual(tr.nearest_stops(x2,y2,dist),
        ['Fyristorg', 'Stationsgatan', 'Samariterhemmet', 'Centralstationen',
        'Dragarbrunn', 'Stadshuset', 'Klostergatan'])
        print "Test - OK ... Finding nearest stops"

    def test_calculate_distance_departure(self):
        tr.nearest_stops_dep = []
        tr.nearest_stops_arr = []
        tr.selected_centroids = [array([ 0.45161914,  0.52874184,  0.55135584,
        0.50578817,  0.172007  ,  0.0162836 ,  0.18377792,  0.0129053 ]),
        array([ 0.43406424,  0.53152554,  0.23595767,  0.61999794,  0.04638085,
        0.17973951,  0.05322643,  0.16249825]),
        array([ 0.5511221 ,  0.51158863,  0.44533246,  0.52734338,  0.11118081,
        0.44409996,  0.10121861,  0.4370837 ]),
        array([ 0.56304867,  0.50875958,  0.49079012,  0.51340253,  0.38025537,
        0.03755701,  0.38917885,  0.04317823])]
        for i in range(len(tr.selected_centroids)):
            cent_lat, cent_long = tr.back_to_coordinates(
            tr.selected_centroids[i][0],tr.selected_centroids[i][1])
            tr.nearest_stops_dep.append(tr.nearest_stops(
            cent_lat, cent_long, 200))
            cent_lat, cent_long = tr.back_to_coordinates(
            tr.selected_centroids[i][2],tr.selected_centroids[i][3])
            tr.nearest_stops_arr.append(tr.nearest_stops(
            cent_lat, cent_long, 200))
        x = [(0.236022142857145, 0.6218945454545409, 0.40896343421923104,
        0.44295239459832625, u'Arrheniusplan'),
        (0.238678571428556, 0.5870136363636353, 0.40812001002704273,
        0.44364416445906113, u'Djursjukhuset'),
        (0.2546271428571387, 0.5872218181818116, 0.40727357545778864,
        0.4443322476140367, u'Campus Ultuna'),
        (0.2753349999999992, 0.5840540909090949, 0.4064241466263627,
        0.44501663096314165, u'Veterin\xe4rv\xe4gen'),
        (0.3359407142856987, 0.5639872727272691, 0.4047163709212964,
        0.4463742461957367, u'Ekudden'),
        (0.34959714285715, 0.5507245454545474, 0.4038580565612437,
        0.4470474522321898, u'Kronparksg\xe5rden'),
        (0.36905928571425406, 0.5455418181818119, 0.40299681296557566,
        0.4477169067691902, u'Gustaf Kjellbergs v\xe4g'),
        (0.3865264285714416, 0.5455240909090874, 0.4012656037101964,
        0.449044510434701, u'Emmy Rappes v\xe4g'),
        (0.39794999999997865, 0.543904545454542, 0.40039567101021384,
        0.4497026342875515, u'Uppsala Folkh\xf6gskola'),
        (0.4188514285714396, 0.5506949999999958, 0.39864723227667076,
        0.4510074633850332, u'Lundellska skolan'),
        (0.43012357142855484, 0.5347072727272748, 0.3977687595308634,
        0.45165414378759955, u'Polacksbacken'),
        (0.42828428571429433, 0.49847272727272374, 0.3968874734808786,
        0.4522969849859463, u'Grindstugan'),
        (0.45128642857140344, 0.49310363636362675, 0.395116528635283,
        0.453571100888228, u'Uppsala Science Park'),
        (0.5006285714285578, 0.5147454545454487, 0.3942269035559092,
        0.4542023513348327, u'Akademiska sjukhuset s\xf6dra'),
        (0.4981964285714144, 0.5162363636363563, 0.3933345326041903,
        0.4548297140630195, u'Akademiska sjukhuset'),
        (0.5175778571428252, 0.5021068181818119, 0.3924394327695829,
        0.4554531771287061, u'Svandammen'),
        (0.5421178571428472, 0.5200304545454572, 0.39154162109349755,
        0.45607272866205456, u'B\xe4verns gr\xe4nd'),
        (0.5531264285714069, 0.5268077272727204, 0.3906411146689745,
        0.45668835686769677, u'Centralstationen')]
        result = tr.calculate_distance_departure(x)
        result['dist_departure'][0] = round(result['dist_departure'][0],4)
        result['dist_departure'][1] = round(result['dist_departure'][1],4)
        result['dist_departure'][2] = round(result['dist_departure'][2],4)
        result['dist_departure'][3] = round(result['dist_departure'][3],4)
        self.assertEqual(result,
        {'pos_departure': [10, 10, 0, 0],
        'dist_departure': [round(0.39325154092790038, 4),
        round(0.35549964732135958,4), 1000, 1000]})
        print "Test - OK ... Distance departure function"

    def test_calculate_distance_arrival(self):
        tr.nearest_stops_dep = []
        tr.nearest_stops_arr = []
        tr.selected_centroids = [array([ 0.45161914,  0.52874184,  0.55135584,
        0.50578817,  0.172007  ,  0.0162836 ,  0.18377792,  0.0129053 ]),
        array([ 0.43406424,  0.53152554,  0.23595767,  0.61999794,  0.04638085,
        0.17973951,  0.05322643,  0.16249825]),
        array([ 0.5511221 ,  0.51158863,  0.44533246,  0.52734338,  0.11118081,
        0.44409996,  0.10121861,  0.4370837 ]),
        array([ 0.56304867,  0.50875958,  0.49079012,  0.51340253,  0.38025537,
        0.03755701,  0.38917885,  0.04317823])]
        for i in range(len(tr.selected_centroids)):
            cent_lat, cent_long = tr.back_to_coordinates(
            tr.selected_centroids[i][0], tr.selected_centroids[i][1])
            tr.nearest_stops_dep.append(tr.nearest_stops(
            cent_lat, cent_long, 200))
            cent_lat, cent_long = tr.back_to_coordinates(
            tr.selected_centroids[i][2],tr.selected_centroids[i][3])
            tr.nearest_stops_arr.append(tr.nearest_stops(
            cent_lat, cent_long, 200))
        x = [(0.236022142857145, 0.6218945454545409, 0.40896343421923104,
        0.44295239459832625, u'Arrheniusplan'),
        (0.238678571428556, 0.5870136363636353, 0.40812001002704273,
        0.44364416445906113, u'Djursjukhuset'),
        (0.2546271428571387, 0.5872218181818116, 0.40727357545778864,
        0.4443322476140367, u'Campus Ultuna'),
        (0.2753349999999992, 0.5840540909090949, 0.4064241466263627,
        0.44501663096314165, u'Veterin\xe4rv\xe4gen'),
        (0.3359407142856987, 0.5639872727272691, 0.4047163709212964,
        0.4463742461957367, u'Ekudden'),
        (0.34959714285715, 0.5507245454545474, 0.4038580565612437,
        0.4470474522321898, u'Kronparksg\xe5rden'),
        (0.36905928571425406, 0.5455418181818119, 0.40299681296557566,
        0.4477169067691902, u'Gustaf Kjellbergs v\xe4g'),
        (0.3865264285714416, 0.5455240909090874, 0.4012656037101964,
        0.449044510434701, u'Emmy Rappes v\xe4g'),
        (0.39794999999997865, 0.543904545454542, 0.40039567101021384,
        0.4497026342875515, u'Uppsala Folkh\xf6gskola'),
        (0.4188514285714396, 0.5506949999999958, 0.39864723227667076,
        0.4510074633850332, u'Lundellska skolan'),
        (0.43012357142855484, 0.5347072727272748, 0.3977687595308634,
        0.45165414378759955, u'Polacksbacken'),
        (0.42828428571429433, 0.49847272727272374, 0.3968874734808786,
        0.4522969849859463, u'Grindstugan'),
        (0.45128642857140344, 0.49310363636362675, 0.395116528635283,
        0.453571100888228, u'Uppsala Science Park'),
        (0.5006285714285578, 0.5147454545454487, 0.3942269035559092,
        0.4542023513348327, u'Akademiska sjukhuset s\xf6dra'),
        (0.4981964285714144, 0.5162363636363563, 0.3933345326041903,
        0.4548297140630195, u'Akademiska sjukhuset'),
        (0.5175778571428252, 0.5021068181818119, 0.3924394327695829,
        0.4554531771287061, u'Svandammen'),
        (0.5421178571428472, 0.5200304545454572, 0.39154162109349755,
        0.45607272866205456, u'B\xe4verns gr\xe4nd'),
        (0.5531264285714069, 0.5268077272727204, 0.3906411146689745,
        0.45668835686769677, u'Centralstationen')]
        result = tr.calculate_distance_arrival(x,
        tr.calculate_distance_departure(x)["pos_departure"])
        result['dist_arrival'][0] = round(result['dist_arrival'][0],4)
        result['dist_arrival'][1] = round(result['dist_arrival'][1],4)
        result['dist_arrival'][2] = round(result['dist_arrival'][2],4)
        result['dist_arrival'][3] = round(result['dist_arrival'][3],4)
        self.assertEqual(result, {'dist_arrival':
        [1000.0, 1000.0, 0.2384, 1000.0], 'pos_arrival': [0, 0, 10, 0]})
        print "Test - OK ... Distance arrival function"

    def test_recommendations_to_return(self):
        tr.to_return = []
        rec = [[ObjectId('566a87b4f073975608b4d460'),
        0.056501097198321068, 7, 17], [ObjectId('566fef25f073971bc714d54b'),
        0.056654373530264993, 7, 17], [ObjectId('566a87b4f073975608b4d461'),
        0.057035859046700416, 7, 17], [ObjectId('566a87b4f073975608b4d45f'),
        0.057107545436496335, 7, 17], [ObjectId('56715f8cf073973ac7776050'),
        0.058394702228002443, 7, 17], [ObjectId('566f3527d3d31e5f74a9721d'),
        0.27146553212609686, 0, 7], [ObjectId('566a87b4f073975608b4d47b'),
        0.27148568827144104, 0, 7], [ObjectId('566f3527d3d31e5f74a9721e'),
        0.27171498213820977, 0, 7], [ObjectId('566f3527d3d31e5f74a9721c'),
        0.27176310376158269, 0, 7], [ObjectId('56715f8cf073973ac777605a'),
        0.27191279288419545, 0, 7]]
        tr.recommendations_to_return(rec)
        self.assertEqual(tr.to_return, [(1, 1, u'Polacksbacken',
        u'Arrheniusplan', [u'Polacksbacken', u'Lundellska skolan',
        u'Uppsala Folkh\xf6gskola', u'Emmy Rappes v\xe4g',
        u'Gustaf Kjellbergs v\xe4g', u'Kronparksg\xe5rden', u'Ekudden',
        u'Veterin\xe4rv\xe4gen', u'Campus Ultuna', u'Djursjukhuset',
        u'Arrheniusplan'], datetime.datetime(2015, 12, 11, 13, 19, 54),
        datetime.datetime(2015, 12, 11, 13, 31, 54),
        ObjectId('566a87b4f073975608b4d460')),
        (1, 1, u'Polacksbacken', u'Arrheniusplan', [u'Polacksbacken',
        u'Lundellska skolan', u'Uppsala Folkh\xf6gskola', u'Emmy Rappes v\xe4g',
         u'Gustaf Kjellbergs v\xe4g', u'Kronparksg\xe5rden', u'Ekudden',
         u'Veterin\xe4rv\xe4gen', u'Campus Ultuna', u'Djursjukhuset',
         u'Arrheniusplan'], datetime.datetime(2015, 12, 15, 13, 17, 28),
         datetime.datetime(2015, 12, 15, 13, 29, 28),
         ObjectId('566fef25f073971bc714d54b')), (1, 1, u'Polacksbacken',
         u'Arrheniusplan', [u'Polacksbacken', u'Lundellska skolan',
         u'Uppsala Folkh\xf6gskola', u'Emmy Rappes v\xe4g',
         u'Gustaf Kjellbergs v\xe4g', u'Kronparksg\xe5rden', u'Ekudden',
         u'Veterin\xe4rv\xe4gen', u'Campus Ultuna', u'Djursjukhuset',
         u'Arrheniusplan'], datetime.datetime(2015, 12, 11, 13, 24, 54),
         datetime.datetime(2015, 12, 11, 13, 36, 54),
         ObjectId('566a87b4f073975608b4d461')), (1, 1, u'Polacksbacken',
         u'Arrheniusplan', [u'Polacksbacken', u'Lundellska skolan',
         u'Uppsala Folkh\xf6gskola', u'Emmy Rappes v\xe4g',
         u'Gustaf Kjellbergs v\xe4g', u'Kronparksg\xe5rden', u'Ekudden',
         u'Veterin\xe4rv\xe4gen', u'Campus Ultuna', u'Djursjukhuset',
         u'Arrheniusplan'], datetime.datetime(2015, 12, 11, 13, 14, 54),
         datetime.datetime(2015, 12, 11, 13, 26, 54),
         ObjectId('566a87b4f073975608b4d45f')),
         (1, 1, u'Polacksbacken', u'Arrheniusplan', [u'Polacksbacken',
         u'Lundellska skolan', u'Uppsala Folkh\xf6gskola',
         u'Emmy Rappes v\xe4g', u'Gustaf Kjellbergs v\xe4g',
         u'Kronparksg\xe5rden', u'Ekudden', u'Veterin\xe4rv\xe4gen',
         u'Campus Ultuna', u'Djursjukhuset', u'Arrheniusplan'],
         datetime.datetime(2015, 12, 16, 13, 29, 13),
         datetime.datetime(2015, 12, 16, 13, 41, 13),
         ObjectId('56715f8cf073973ac7776050')), (1, 1, u'Centralstationen',
         u'Polacksbacken', [u'Centralstationen', u'B\xe4verns gr\xe4nd',
         u'Svandammen', u'Akademiska sjukhuset',
         u'Akademiska sjukhuset s\xf6dra', u'Uppsala Science Park',
         u'Grindstugan', u'Polacksbacken'],
         datetime.datetime(2015, 12, 14, 16, 46, 57),
         datetime.datetime(2015, 12, 14, 16, 55, 57),
         ObjectId('566f3527d3d31e5f74a9721d')), (1, 1, u'Centralstationen',
         u'Polacksbacken', [u'Centralstationen', u'B\xe4verns gr\xe4nd',
         u'Svandammen', u'Akademiska sjukhuset',
         u'Akademiska sjukhuset s\xf6dra', u'Uppsala Science Park',
         u'Grindstugan', u'Polacksbacken'],
         datetime.datetime(2015, 12, 11, 16, 45, 20),
         datetime.datetime(2015, 12, 11, 16, 54, 20),
         ObjectId('566a87b4f073975608b4d47b')), (1, 1, u'Centralstationen',
         u'Polacksbacken', [u'Centralstationen', u'B\xe4verns gr\xe4nd',
         u'Svandammen', u'Akademiska sjukhuset',
         u'Akademiska sjukhuset s\xf6dra', u'Uppsala Science Park',
         u'Grindstugan', u'Polacksbacken'],
         datetime.datetime(2015, 12, 14, 16, 53, 57),
         datetime.datetime(2015, 12, 14, 17, 2, 57),
         ObjectId('566f3527d3d31e5f74a9721e')), (1, 1, u'Centralstationen',
         u'Polacksbacken', [u'Centralstationen', u'B\xe4verns gr\xe4nd',
         u'Svandammen', u'Akademiska sjukhuset',
         u'Akademiska sjukhuset s\xf6dra', u'Uppsala Science Park',
         u'Grindstugan', u'Polacksbacken'],
         datetime.datetime(2015, 12, 14, 16, 39, 57),
         datetime.datetime(2015, 12, 14, 16, 48, 57),
         ObjectId('566f3527d3d31e5f74a9721c')), (1, 1, u'Centralstationen',
         u'Polacksbacken', [u'Centralstationen', u'B\xe4verns gr\xe4nd',
         u'Svandammen', u'Akademiska sjukhuset',
         u'Akademiska sjukhuset s\xf6dra', u'Uppsala Science Park',
         u'Grindstugan', u'Polacksbacken'],
         datetime.datetime(2015, 12, 16, 16, 56, 13),
         datetime.datetime(2015, 12, 16, 17, 5, 13),
         ObjectId('56715f8cf073973ac777605a'))])
        print "Test - OK ... Recommendations to return"

    def test_to_seconds(self):
        a = datetime.datetime(2015,1,1,0,0,1)
        b = datetime.datetime(2000,2,3,23,59,59)
        self.assertTrue(tr.to_seconds(a), 1)
        self.assertTrue(tr.to_seconds(b), 86399)
        print "Test - OK ... Datetime conversion to seconds"

    def test_to_coordinates(self):
        a = 0
        b = 21600
        c = 43200
        d = 86400
        self.assertTrue(tr.to_coordinates(a), (13750, 0))
        self.assertTrue(tr.to_coordinates(b), (0, 13750))
        self.assertTrue(tr.to_coordinates(c), (-13750, 0))
        self.assertTrue(tr.to_coordinates(d), (0, -13750))
        print "Test - OK ... Seconds conversion to coordinates"

    def test_time_normalizer(self):
        a = 13750
        b = -12345
        c = 83000
        self.assertTrue(tr.to_coordinates(a), 0.5)
        self.assertTrue(tr.to_coordinates(b), 0.025545454545454545)
        self.assertTrue(tr.to_coordinates(c), 1.759090909090909)
        print "Test - OK ... Time normalization"

    def test_lat_normalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(tr.lat_normalizer(a), 0.5089428571428637)
        self.assertTrue(tr.lat_normalizer(b), 0.4316214285714063)
        self.assertTrue(tr.lat_normalizer(c), -426.9999999999983)
        print "Test - OK ... Latitude normalization"

    def test_lon_normalizer(self):
        a = 59.851252
        b = 59.840427
        c = 0
        self.assertTrue(tr.lat_normalizer(a), 192.36932727272827)
        self.assertTrue(tr.lat_normalizer(b), 192.3201227272737)
        self.assertTrue(tr.lat_normalizer(c), -79.6818181818186)
        print "Test - OK ... Longitude normalization"

    def test_remove_duplicates(self):
        a = [(1,2,1,2), (1,2,1,2), (1,2,1,2), (2,3,4,5)]
        b = [(1,2,3,4), (1,2,3,4), (1,2,3,4)]
        self.assertEqual(tr.remove_duplicates(a), [(2,4,5), (1,1,2)])
        self.assertEqual(tr.remove_duplicates(b), [(1,3,4)])
        print "Test - OK ... Removing duplicates"

    def test_time_approximation(self):
        self.assertEqual(tr.time_approximation(59.851252, 17.593290,
                                              59.858052, 17.644739), 18)
        self.assertEqual(tr.time_approximation(59.851252, 17.593290,
                                              59.840427, 17.647628), 20)
        print "Test - OK ... Approximating time"

    def test_back_to_coordinates(self):
        a = 0.5089428571428637
        b = 0.28768181818181293
        self.assertEqual(tr.back_to_coordinates(a,b), (59.851252, 17.59329))
        print "Test - OK ... Back to coordinates"

if __name__ == "__main__":
    unittest.main()
