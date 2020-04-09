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

        self.casting_assistant_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6I'
                                        'kpXVCIsImtpZCI6Ik5qSTJOVFJHT0VSQ01FU'
                                        'XlPVU5DUVVVM09EQTRSREJCUmtVeE5rRTBPV'
                                        'EZFT1VJM1FUUTRPUSJ9.eyJpc3MiOiJodHRw'
                                        'czovL2Rldi1rYWY4MTBsby5hdXRoMC5jb20v'
                                        'Iiwic3ViIjoiYXV0aDB8NWU4Y2ViNjBhYjY2'
                                        'MTEwYzBhMWU4ODAyIiwiYXVkIjoiYWdlbmN5'
                                        'IiwiaWF0IjoxNTg2Mzg3Mjc0LCJleHAiOjE1'
                                        'ODY0NzM2NzQsImF6cCI6IjFxRjZ1c0RrUjRE'
                                        'QUpUOXVzTGZQRVAyOXpMeTVJTGZaIiwic2Nv'
                                        'cGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6'
                                        'YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.m6IeN'
                                        'HJBDdzn3JdStt7pznC_sFh0y3ASMx2YDu9ZR'
                                        'jEGO82fnISn1zCd-OSBQ__AiFcmqR60HtRKl'
                                        '8hShufkfo_bLuXeCxg9NKrNgXuQAAbLYEqPw'
                                        'GpxUdIE7c_3sbO7-k5iZXDfaZxe31YQP0kIz'
                                        'oYOUlnGmKyQTXWT7ePdTW5GxzWk3F0AOQGd0'
                                        'Dh4q686CwFFvfoKtMr5OkgJu7cgp-ONWu9BM'
                                        'tDCFzgwyeG4itli8a05yJmtpdtyBJodkfwzG'
                                        'OC2Xds_utPPZKBcFaWbnXFRi89vPgQcl3ukJ'
                                        'yD1ak4xrf2xs4jXf0q2-BaRuT_tWHE1jDdWk'
                                        'INiI1sqxtdF9Q')

        self.casting_director_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ik'
                                       'pXVCIsImtpZCI6Ik5qSTJOVFJHT0VSQ01FUXl'
                                       'PVU5DUVVVM09EQTRSREJCUmtVeE5rRTBPVEZF'
                                       'T1VJM1FUUTRPUSJ9.eyJpc3MiOiJodHRwczov'
                                       'L2Rldi1rYWY4MTBsby5hdXRoMC5jb20vIiwic'
                                       '3ViIjoiYXV0aDB8NWU4N2NhY2NmMjNiYzIwYm'
                                       'YwY2IxY2MwIiwiYXVkIjoiYWdlbmN5IiwiaWF'
                                       '0IjoxNTg2Mzg3MTc3LCJleHAiOjE1ODY0NzM1'
                                       'NzcsImF6cCI6IjFxRjZ1c0RrUjREQUpUOXVzT'
                                       'GZQRVAyOXpMeTVJTGZaIiwic2NvcGUiOiIiLC'
                                       'JwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3J'
                                       'zIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMi'
                                       'LCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZ'
                                       'XMiLCJwb3N0OmFjdG9ycyJdfQ.HvP2KVaQmXm'
                                       'OtzH05Qol7ORsgOQMTDSLJy9gJVN9dBtdgBu1'
                                       'Z6d_sabkLvE4TUKkyNwCRk_J3XH3Yr4XJ1mJf'
                                       'DZArZ_cxn1m23cX0cezWDYwOfHiH9hKUvzdKy'
                                       'XgLDQviGVUZK6kQAQuONSxzlnJ5ICQgfBx5ht'
                                       'TdMZFIp8WYHOmmzW83WeFasblOByPvxw--S89'
                                       'VdfZR0Dj1bC0yiCu3jtMn8nK0sPlNrZy4pscC'
                                       '9evHcj2A9-VGNctSaKgYrKOnt4VMLU3qteX0q'
                                       'KR7HjR4MxT02wjl_WyqXxqpQQdy5kMOGfy9zE'
                                       'xN5g5bp3ZtgV6bgJ3CIRBZ_F7gMFdGscTtg')

        self.excecutive_producer_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI'
                                          '6IkpXVCIsImtpZCI6Ik5qSTJOVFJHT0VSQ'
                                          '01FUXlPVU5DUVVVM09EQTRSREJCUmtVeE5'
                                          'rRTBPVEZFT1VJM1FUUTRPUSJ9.eyJpc3Mi'
                                          'OiJodHRwczovL2Rldi1rYWY4MTBsby5hdX'
                                          'RoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4'
                                          'M2ZmNzM2YjI2OWEwYmRjMDhjYWFkIiwiYX'
                                          'VkIjoiYWdlbmN5IiwiaWF0IjoxNTg2Mzg3'
                                          'MDQyLCJleHAiOjE1ODY0NzM0NDIsImF6cC'
                                          'I6IjFxRjZ1c0RrUjREQUpUOXVzTGZQRVAy'
                                          'OXpMeTVJTGZaIiwic2NvcGUiOiIiLCJwZX'
                                          'JtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3Jz'
                                          'IiwiZGVsZXRlOm1vdmllcyIsImdldDphY3'
                                          'RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6'
                                          'YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG'
                                          '9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJd'
                                          'fQ.XJEBjc2qJT8rC24TszQmWFaeJFfnWpD'
                                          'wJv7ZwIhysfku5ej5rD0yT7VtXRPQXNcPr'
                                          'VXiuAekZXZM9fFIpfkll8M3bpZh8TqtCRO'
                                          '079RAUAoNkkWj1LlR1pn49nFU3nVtsS3pJ'
                                          'YLA5zvUPdMQ9B_RK-Az5AULP_EXqE_r7T3'
                                          'fKzvIpjl2tkgiBYN9Bt4cSjAErh1yxfFvx'
                                          'dWUYt3EiMhVADyLqIbtupx9lyi8S9Qlj5T'
                                          'hfqJr8nqoTjF5AuDeofe5SIlDs0wMWe3oJ'
                                          'opfMrMatv4lX6pcdbHS9PBADdcWsMjAoMl'
                                          'cMNAbCl6v5mTc2t9fD1B6St01vOFnn_TTW'
                                          '2V5ug')

    def tearDown(self):
        pass

# ____________Movies test____________

    def test_show_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.casting_assistant_token,
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
                                     self.excecutive_producer_token,
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
                                      self.excecutive_producer_token,
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
                                      self.excecutive_producer_token,
                                      'Content-Type': 'Text'
                                      })

        self.assertEqual(res.status_code, 404)

    def test_fail_delete_movie(self):
        res = self.client().delete('/movies/3987203',
                                   headers={
                                       'Authorization':
                                       self.excecutive_producer_token,
                                       'Content-Type': 'Text'
                                       })

        self.assertEqual(res.status_code, 404)

    # ____________Actors test____________
    def test_show_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.casting_assistant_token,
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
                                     self.casting_director_token,
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
                                      self.casting_director_token,
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
                                      self.casting_director_token,
                                      'Content-Type': 'Text'
                                      })

        self.assertEqual(res.status_code, 404)

    def test_fail_delete_actor(self):
        res = self.client().delete('/actors/3987203',
                                   headers={
                                       'Authorization':
                                       self.casting_director_token,
                                       'Content-Type': 'Text'
                                       })

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
