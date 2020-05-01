#heroku restart; heroku pg:reset DATABASE --confirm sheffercapstone; heroku run rake db:migrate

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date




casting_director_token ='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FRTBRakpEUXpjM05qSTRNVEV5UlRRelEwVTRNa0ZDUmpKRVFUQTFSVVkwTnpJek1VSkdRdyJ9.eyJpc3MiOiJodHRwczovL2pvbnNoZWZmZXIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNWVkNGZmY2U5YzgyMGQ1ZTFjNzkzZCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4MzcwMzM2LCJleHAiOjE1ODg0NTY3MDMsImF6cCI6IlBaMDA5WkcyRVc4bjVkaXBPR3JkdXExbEVBbzNQRkpiIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.dXpsHZJAhbsQqDiEnMdmiK46_rlu_YO2C_0zC4nzXKzJ_mvORZNpHKeIIQINOLw51Mv2MByC-juM8cvNmVLryilqyF-cJxVOobKn08d4hvBYrs99Pw8FuJKO-5nLogBX2M3qJgvdfmNjxuMx3EY9HJz3zdnnBECCe-nN2cM02LOzfN8HKgnCjbxUt5Y1fO6ifUdu9h2qtKLAqNYqzGmrWwtg5gbrLZqgWWtwhLdF46pnU6MADePE_bc-InK98FjHbfxMygHfCFQyx0EEh34eHSBtfvQw9MlgCfXBEou4G6gOOrX356TVizfJ5DaWPMwBKnHAc10BZmNJyWVP1Er6zA'
executive_producer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FRTBRakpEUXpjM05qSTRNVEV5UlRRelEwVTRNa0ZDUmpKRVFUQTFSVVkwTnpJek1VSkdRdyJ9.eyJpc3MiOiJodHRwczovL2pvbnNoZWZmZXIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNWVkNGQyODhlYzE3MGQ2YjhmMjZiNCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4MzcwMTgyLCJleHAiOjE1ODg0NTY1NDksImF6cCI6IlBaMDA5WkcyRVc4bjVkaXBPR3JkdXExbEVBbzNQRkpiIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.t3DtJ-5Si9iudn-Kxh8Fh5aSuL4RVZrJBe1hX7_pEs7GvH3XVLOyOF2_2WH9GdyLdE9_m02Gv6DWPxO5jIa01TDSrMciZ62nir0qoCMCsj5u36I86oDsNoVCvMbXoauc6QOEFdjvaQUmKbqNGzYTRDJXzswfettdol3Gjli2m-Fr-CA75G8E5lU29gkmX4d4jBCVSU1s3Bz1nKlaI_PuFnboSEIfXxHBak7n_p2GPA1meQ_CM0bLvit_xD1l-s-z0aUp8gWf5zq9BjkgWHPB72adyGo2lQ106AG_Cms388LCmLNZcKMtXez-eEJKeRLOUOPsNfCEMkSqrrUrphtsVg'
director_auth_header =  { 'Authorization': casting_director_token }
executive_auth_header = { 'Authorization': executive_producer_token }

# new_movie = {"id": 10, "title": "Fake_movie", "release_date": "2020-04-10"}
# new_actor = {"id": 10, "name": "Fake Actor", "age": 29, "gender": "Male"}

class CastingTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgres://iegqbkuxwfvlyx:86b85be0622cb66b45a2a7f5ce775642d455431a8fb3c7a4e62f576cc4061ff1@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d9ddjavkel9st9'
        setup_db(self.app, self.database_path)

        self.new_movie = {"id": 10, "title": "Fake_movie", "release_date": "2020-04-10"}
        self.new_actor = {"id": 10, "name": "Fake Actor", "age": 29, "gender": "Male"}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # def test_create_new_movies_executive_producer(self):

    #     res = self.client().get('/movies', headers=executive_auth_header)
    #     data = json.loads(res.data)
    #     #print(res.headers)
    #     self.assertEqual(res.status_code, 200)

    #     self.assertEqual(data['success'], True)
    # # tests for POST /actors

    def test_a_add_actor(self):
        # add new actors: success case
        res = self.client().post(
            "/actors", json=self.new_actor, headers=director_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor_id"],1)

    def test_a_add_actor_401(self):
        # add new actor: failure ,without authorization header
        res = self.client().post("/actors", json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")


    # tests for GET /actors
    def test_b_get_actors(self):
        # get actors
        res = self.client().get("/actors", headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["actors"]), 1)

    # tests for GET /actors
    def test_b_get_actors_401(self):
        # get actors
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")
    # tests for PATCH /actors
    def test_c_patch_actors(self):
        # update an actor , sending id and json
        this_actor = {"name": "Matt Damon"}
        res = self.client().patch(
            "/actors/1", json=self.new_actor, headers=executive_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor_id"], 1)

    def test_c_patch_actors_404(self):
        # update an actor , not sending json
        res = self.client().patch("/actors/10", headers=executive_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")


    # tests for DELETE /actors
    def test_d_delete_actor(self):
        # delete an actor , failure scenario: incorrect actor_id
        res = self.client().delete("/actors/1", headers=executive_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor_id"], 1)

    def test_d_delete_actor_401(self):
        # delete an actor , without headers
        res = self.client().delete("/actors/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")




    # tests for POST /movies

    def test_a_add_movie(self):
        # add new movies: success case
        res = self.client().post("/movies", json=self.new_movie, headers=executive_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie_id"],1)

    def test_a_add_movie_403(self):
        res = self.client().post("/movies", json=self.new_movie, headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "no_permission")


    # tests for GET /actors
    def test_b_get_movies(self):
        # get actors
        res = self.client().get("/movies", headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["movies"]), 1)

    def test_b_get_movies_403(self):
        # get actors
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")

    # tests for PATCH /movies
    def test_c_patch_movies(self):
        # update an actor , sending id and json
        this_actor = {"title": "Pulp Fiction"}
        res = self.client().patch(
            "/movies/1", json=self.new_actor, headers=executive_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie_id"], 1)

    def test_c_patch_movies_404(self):
        # update an actor , not sending json
        res = self.client().patch("/movies/10", headers=executive_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")


    # tests for DELETE /movies

    def test_d_delete_actor_403(self):
        # delete an actor , without headers
        res = self.client().delete("/movies/1", headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "no_permission")

    def test_d_delete_movie(self):
        # delete an actor , failure scenario: incorrect actor_id
        res = self.client().delete("/movies/1", headers=executive_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie_id"], 1)




if __name__ == "__main__":
    unittest.main()