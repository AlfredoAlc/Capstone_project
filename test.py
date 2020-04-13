import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth


class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = 'postgres://aar92_22@localhost:5432/agencyDB'
        self.database_path = ('postgres://sjtmsunvoblvdc:28616399cc7bd7b269a'
                              '82fbcace62d274cb65f500eda8f8ba35946afe960d1e8'
                              '@ec2-35-171-31-33.compute-1.amazonaws.com:543'
                              '2/d857cptkuo45vv')

        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_movie = {
            'title': 'Fast & Furious',
            'release_date': '2001'
        }

        self.new_actor = {
            'name': 'Jack',
            'age': 27,
            'gender': 'Male'
        }

        self.assistant_t = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ik'
                            'pXVCIsImtpZCI6Ik5qSTJOVFJHT0VSQ01FUXl'
                            'PVU5DUVVVM09EQTRSREJCUmtVeE5rRTBPVEZF'
                            'T1VJM1FUUTRPUSJ9.eyJpc3MiOiJodHRwczov'
                            'L2Rldi1rYWY4MTBsby5hdXRoMC5jb20vIiwic'
                            '3ViIjoiYXV0aDB8NWU4Y2ViNjBhYjY2MTEwYz'
                            'BhMWU4ODAyIiwiYXVkIjoiYWdlbmN5IiwiaWF'
                            '0IjoxNTg2NzQwODA2LCJleHAiOjE1ODY4Mjcy'
                            'MDYsImF6cCI6IjFxRjZ1c0RrUjREQUpUOXVzT'
                            'GZQRVAyOXpMeTVJTGZaIiwic2NvcGUiOiIiLC'
                            'JwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiw'
                            'iZ2V0Om1vdmllcyJdfQ.ZrCyd-2II5fbsoLcs'
                            '6nW_LGA6GZ5isHcPhZQcuH35Tw4WDBeJY3HBK'
                            'p7TGBhVGdE6t2GB40ZbM8kl42JuWcUR4l8fIP'
                            'TdAtNvwtRvtuFqscJo62DHAdfV4V01nsFyjmz'
                            'fQCP5OKlhR7Drv0kQH2ESfb2ZkfC84wrHLVdo'
                            '1DCuYZQvdbB_q7S4ckheY1apBUUJzQ9FUu_e2'
                            '9jTgyaXEZ5pmsX6m8oUdgcW6COpUBzXJPLVhT'
                            'nzTNo6mW_zzFFrkK-9N3QRp13thxFVwYU4a0R'
                            'pht3qSUth7QuWpt4i1plyqiTqHgfKz8QNBAZN'
                            '-snh-uOMHcjgMzthwuqxbchH6oqGw')

        self.directort = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6'
                          'Ik5qSTJOVFJHT0VSQ01FUXlPVU5DUVVVM09EQTRSREJCUmtVeE5'
                          'rRTBPVEZFT1VJM1FUUTRPUSJ9.eyJpc3MiOiJodHRwczovL2Rld'
                          'i1rYWY4MTBsby5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4'
                          'N2NhY2NmMjNiYzIwYmYwY2IxY2MwIiwiYXVkIjoiYWdlbmN5Iiw'
                          'iaWF0IjoxNTg2NzQwNzQzLCJleHAiOjE1ODY4MjcxNDMsImF6cC'
                          'I6IjFxRjZ1c0RrUjREQUpUOXVzTGZQRVAyOXpMeTVJTGZaIiwic'
                          '2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3Jz'
                          'IiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3R'
                          'vcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.AH5'
                          'CHv9KgJLrB-plUSOPL_E_eyszhI2hHHOUlxnyqKc1pZrsO7fqxw'
                          'Yhn1TbDu8k4TFKDyTTyugXCclCUrtik1n8Cs61nOtnVqQUtLKMd'
                          'JM79K4o8-fNDR4ClxYSFlZh7LkJuopi5Kr2aAWjNLkN4bsz1jrI'
                          'MtP3N74--yRpHVxjiv80AqmYR8OL0nYiU-f1iCdnFy9__QUHjN2'
                          'qs70fjbxaLifOHYpL4f507aJLrtbmVaTsJtOz8gflbeaIWTMyAl'
                          'i8Q-B7YE-KAyuvOn4K4bCT8aUAKUrotHd1DhD7ohbfJyvrmNasf'
                          'iCvP2dwJUTto-5WcrFBP4pB9iC60RA_QQ')

        self.producert = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6'
                          'Ik5qSTJOVFJHT0VSQ01FUXlPVU5DUVVVM09EQTRSREJCUmtVeE5'
                          'rRTBPVEZFT1VJM1FUUTRPUSJ9.eyJpc3MiOiJodHRwczovL2Rld'
                          'i1rYWY4MTBsby5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4'
                          'M2ZmNzM2YjI2OWEwYmRjMDhjYWFkIiwiYXVkIjoiYWdlbmN5Iiw'
                          'iaWF0IjoxNTg2NzQwNTkwLCJleHAiOjE1ODY4MjY5OTAsImF6cC'
                          'I6IjFxRjZ1c0RrUjREQUpUOXVzTGZQRVAyOXpMeTVJTGZaIiwic'
                          '2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3Jz'
                          'IiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW9'
                          '2aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG'
                          '9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.OF5dAoM7rBTyv7'
                          'v8pdUohFJ7QyoC2ic__Haf73eQ23UilrGqT7b_vFQH8uL8pTNXL'
                          'yErcXVLBQ-tqR2Ko7LAVbBPSWiXjTSRPvTXuoBLqGwZQLpU1yu3'
                          'wcyB9fHyHqGOAM9WHqThP-h2xuV2fgtMluZwfhvZ-zUpUy9wgax'
                          'p6dOZf6wpxndLut483QzOgF5bfeTOXOpqU2amZzQDXOXjIxTv_r'
                          '5aUuMUXopIEDgxUQGFp7pQzoWUOOITS1Ei7bHd0wGXNk1TOshFX'
                          'gWwBTS1Wne2izLMVIJNNQmCVqLj9nMHFmYcBX1BZrR0msbQEBmj'
                          'WLVjyczjwaEgtofi8tihig')

    def tearDown(self):
        pass

# ____________Movies test____________

    def test_show_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.assistant_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_fail_show_movies(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 500)

    def test_add_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={
                                     'Authorization':
                                     self.producert,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_added'])

    def test_fail_add_movie(self):
        res = self.client().post('/movies')

        self.assertEqual(res.status_code, 500)

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
                                  headers={
                                      'Authorization':
                                      self.producert,
                                      'Content-Type': 'Text'
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_updated'])

    def test_fail_update_movie(self):
        res = self.client().patch('/movies/1098377', json=self.new_movie,
                                  headers={
                                      'Authorization':
                                      self.producert,
                                      'Content-Type': 'Text'
                                      })

        self.assertEqual(res.status_code, 404)

    def test_fail_delete_movie(self):
        res = self.client().delete('/movies/3987203',
                                   headers={
                                       'Authorization':
                                       self.producert,
                                       'Content-Type': 'Text'
                                       })

        self.assertEqual(res.status_code, 404)

    # ____________Actors test____________
    def test_show_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.assistant_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_fail_show_actors(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 500)

    def test_add_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={
                                     'Authorization':
                                     self.directort,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_added'])

    def test_fail_add_actor(self):
        res = self.client().post('/actors', json=None)

        self.assertEqual(res.status_code, 500)

    def test_update_actors(self):
        res = self.client().patch('/actors/1', json=self.new_actor,
                                  headers={
                                      'Authorization':
                                      self.directort,
                                      'Content-Type': 'Text'
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_updated'])

    def test_fail_update_actor(self):
        res = self.client().patch('/actors/1098377', json=self.new_actor,
                                  headers={
                                      'Authorization':
                                      self.directort,
                                      'Content-Type': 'Text'
                                      })

        self.assertEqual(res.status_code, 404)

    def test_fail_delete_actor(self):
        res = self.client().delete('/actors/3987203',
                                   headers={
                                       'Authorization':
                                       self.directort,
                                       'Content-Type': 'Text'
                                       })

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
