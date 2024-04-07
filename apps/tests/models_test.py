import unittest
from blog import db
from blog.models import User, Post


USERNAME = "test_user"
EMAIL = "test@gmail.com"
PASSWORD = "pass12345"
WRONG_PASS = "Pass54321"


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_password_setting(self):
        user = User(username=USERNAME, email=EMAIL)
        user.password = PASSWORD
        db.session.add(user)
        db.session.commit()
        
        self.assertTrue(user.check_password(PASSWORD))
        self.assertFalse(user.check_password(WRONG_PASS))
        
    def test_password_verification(self):
        with self.assertRaises(ValueError):
            user = User(username=USERNAME, email=EMAIL, password="")
    
    def test_email_uniqueness(self):
        user1 = User(username=USERNAME + "1", email=EMAIL)
        user2 = User(username=USERNAME + "2", email=EMAIL)
        db.session.add(user1)
        with self.assertRaises(Exception):
            db.session.add(user2)
            db.session.commit()


class PostModelTestCase(unittest.TestCase):
    
    def setUp(self):
        db.create_all()
        user = User(username=USERNAME, email=EMAIL)
        user.password = PASSWORD
        db.session.add(user)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_post_creation(self):
        user = User.query.first()
        post = Post(title="Title", content="This is a test post", author=user.id)
        db.session.add(post)
        db.session.commit()
        
        # Assert post creation
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.content, "This is a test post")
        self.assertEqual(post.author, user.id)
        
        # Retrieve post from database
        retrieved_post = Post.query.get(post.id)
        
        # Assert retrieved post date
        self.assertEqual(retrieved_post.title, "Title")
        self.assertEqual(retrieved_post.content, "This is a test post")
        self.assertEqual(retrieved_post.author, user.id)
        

if __name__  == "__main__":
    unittest.main()