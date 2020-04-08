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
        self.database_path = 'postgres://aar92_22@localhost:5432/agencyDB'

        setup_db(self.app, self.database_path)

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

        self.casting_assistant_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cC'
                                        'I6IkpXVCIsImtpZCI6Ik5qSTJOVFJHT0V'
                                        'SQ01FUXlPVU5DUVVVM09EQTRSREJCUmtV'
                                        'eE5rRTBPVEZFT1VJM1FUUTRPUSJ9.eyJp'
                                        'c3MiOiJodHRwczovL2Rldi1rYWY4MTBsb'
                                        'y5hdXRoMC5jb20vIiwic3ViIjoiYXV0aD'
                                        'B8NWU4Y2ViNjBhYjY2MTEwYzBhMWU4ODA'
                                        'yIiwiYXVkIjoiYWdlbmN5IiwiaWF0Ijox'
                                        'NTg2Mjk0ODA4LCJleHAiOjE1ODYzODEyM'
                                        'DgsImF6cCI6IjFxRjZ1c0RrUjREQUpUOX'
                                        'VzTGZQRVAyOXpMeTVJTGZaIiwic2NvcGU'
                                        'iOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6'
                                        'YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.e4'
                                        'wd7A6jM4Ep8jhG6azqjHvTfIDqLHofFGU'
                                        'OHqPfiiKd4sbkFE9avAngyzP2irQI7iRd'
                                        'hs6f0lUrEKucfM3-6WB7B-l0RZp5hhtHM'
                                        'NHrPHJbtxRGT-xNhZi7EwNM37YlNOoD9s'
                                        '-tGpqJPKfDQXD29xUI0MyXT13QeUD0Vja'
                                        '3I76hEyHJTWUXSoR2M4F0kkFNkocmS5Ay'
                                        'SGWoXdVEA236SbjBXKFoiKtDnrw9MkJLm'
                                        '3PAVZCnHCmUnGJ4BjmzyV81Q130OmwOVd'
                                        'QcGCcu1pPw6Yx7GOknwZGCoo2b0YqPlph'
                                        'tfnE8EgAMgoQA4vo_6VqW-Vp42FEek0V5'
                                        'jvisZ560aQ')

        self.casting_director_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI'
                                       '6IkpXVCIsImtpZCI6Ik5qSTJOVFJHT0VSQ'
                                       '01FUXlPVU5DUVVVM09EQTRSREJCUmtVeE5'
                                       'rRTBPVEZFT1VJM1FUUTRPUSJ9.eyJpc3Mi'
                                       'OiJodHRwczovL2Rldi1rYWY4MTBsby5hdX'
                                       'RoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4'
                                       'N2NhY2NmMjNiYzIwYmYwY2IxY2MwIiwiYX'
                                       'VkIjoiYWdlbmN5IiwiaWF0IjoxNTg2Mjk0'
                                       'OTAzLCJleHAiOjE1ODYzODEzMDMsImF6cC'
                                       'I6IjFxRjZ1c0RrUjREQUpUOXVzTGZQRVAy'
                                       'OXpMeTVJTGZaIiwic2NvcGUiOiIiLCJwZX'
                                       'JtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3Jz'
                                       'IiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZX'
                                       'MiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDpt'
                                       'b3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.HP3'
                                       'YcKweZhSes38uUT7pVBoVJx5YX-AALdoVa'
                                       'Jmr74WncFp9AcXXTCxlLOh6m_Xi0uMurWt'
                                       'Ud7O3Gd2SEksreRVm3JmcFoB6F6ceC2X-x'
                                       'ef6-u83FIbCkma9coT-uKYkuLscnO_3-Rn'
                                       'Nak5-tP_0YJ_AahRQuVf_22PdT8WxQ2Yk0'
                                       'G8EqwQ_zEGikPGyio8gmSaitWVxzJ4fdTZ'
                                       '6I13efsdo2Hk8-a5S--lerGaJH_NV7zN1a'
                                       'uajSu-AHT0qeEE6vLJSZelLqh50035XX2O'
                                       'wgRYKARGYb0cVx1qMlohIvTzhzKN7u2swb'
                                       'cLAkgo-s4FFLbnUg74lqLbM_kzop0Amiw')

        self.excecutive_producer_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5'
                                          'cCI6IkpXVCIsImtpZCI6Ik5qSTJOVFJ'
                                          'HT0VSQ01FUXlPVU5DUVVVM09EQTRSRE'
                                          'JCUmtVeE5rRTBPVEZFT1VJM1FUUTRPU'
                                          'SJ9.eyJpc3MiOiJodHRwczovL2Rldi1'
                                          'rYWY4MTBsby5hdXRoMC5jb20vIiwic3'
                                          'ViIjoiYXV0aDB8NWU4M2ZmNzM2YjI2O'
                                          'WEwYmRjMDhjYWFkIiwiYXVkIjoiYWdl'
                                          'bmN5IiwiaWF0IjoxNTg2Mjk0NTYyLCJ'
                                          'leHAiOjE1ODYzODA5NjIsImF6cCI6Ij'
                                          'FxRjZ1c0RrUjREQUpUOXVzTGZQRVAyO'
                                          'XpMeTVJTGZaIiwic2NvcGUiOiIiLCJw'
                                          'ZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN'
                                          '0b3JzIiwiZGVsZXRlOm1vdmllcyIsIm'
                                          'dldDphY3RvcnMiLCJnZXQ6bW92aWVzI'
                                          'iwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6'
                                          'bW92aWVzIiwicG9zdDphY3RvcnMiLCJ'
                                          'wb3N0Om1vdmllcyJdfQ.I_icUJLyCAb'
                                          'E5gwPSMnSWqDglfQIFdwqUvBtvEp0np'
                                          'XwPdH_dHZB737Rkj3G9mfHY2mqNetza'
                                          'm5UQ0E3i2mojKYddA2qqtDGU7DKaepf'
                                          'XbBgY56TQt3WtAjTyCJE4qtLJF1DPAp'
                                          'r0UQQfnJBNNJC-v_9UFYtPNrBO56DO6'
                                          'LprGxwxIzIG9sQBnnNqE9PyAjDHEpLU'
                                          'fPS6U_ozj41ndWSQKLDyOoNcTJWgdgd'
                                          'Dj_jp6Btj32zD79DSTIx08LET16X83R'
                                          'wnMSncvbpPIFd9jR30WviAM1byCZlx2'
                                          'HjYNIlEieD2BukPtiGYmcginLdL63j1'
                                          'wWanh6g9HrA6INjxA2Crw')

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
