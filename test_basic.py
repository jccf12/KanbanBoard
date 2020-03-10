import os
import unittest
 
from project import app, db, ma
 
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        ma.init_app(app)
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.post('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.app.post(
          '/add/addtodo',
          data = dict(taskname="test", description="Hi", dateadded="2019-03-20 04:33:03.817206", lastmodified = "2019-03-20 04:33:03.817206", duedate="2019-03-20", status = "doing"),
          follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_move(self):
        self.test_add()
        response = self.app.get('/move/1/movetodo', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

 
if __name__ == "__main__":
    unittest.main()