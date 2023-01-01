import sys
sys.path.insert(0, '/home/pythinker/Desktop/alx/chemex/src')
import unittest
from datetime import datetime
from src.app import create_app
from database import db, Users, Comments, Replies, Posts

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = Users(firstName='John', lastName='Doe', username='johndoe', 
                          email='johndoe@example.com', password='password123', role='admin')
        db.session.add(self.user)
        db.session.commit()

    def test_user_creation(self):
        self.assertEqual(self.user.firstName, 'John')
        self.assertEqual(self.user.lastName, 'Doe')
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.email, 'johndoe@example.com')
        self.assertEqual(self.user.password, 'password123')
        self.assertEqual(self.user.role, 'admin')
        self.assertIsInstance(self.user.createdAt, datetime)
        self.assertIsInstance(self.user.updatedAt, datetime)
        self.assertEqual(self.user.createdAt, self.user.updatedAt)

    def test_user_repr(self):
        self.assertEqual(str(self.user), '<User johndoe>')

    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()

    def test_unique_email(self):
        user2 = Users(firstName='Jane', lastName='Doe', username='janedoe', 
                      email='johndoe@example.com', password='password123')
        db.session.add(user2)
        with self.assertRaises(Exception) as context:
            db.session.commit()
        self.assertTrue('UNIQUE constraint failed: users.email' in str(context.exception))
        db.session.rollback()

    def test_unique_username(self):
            user2 = Users(firstName='Jane', lastName='Doe', username='johndoe', 
                        email='janedoe@example.com', password='password123')
            db.session.add(user2)
            with self.assertRaises(Exception) as context:
                db.session.commit()
            self.assertTrue('UNIQUE constraint failed: users.username' in str(context.exception))
            db.session.rollback()


    def test_password_hashing(self):
        user2 = Users(firstName='Jane', lastName='Doe', username='janedoe', 
                      email='janedoe@example.com', password='password123')
        db.session.add(user2)
        db.session.commit()
        self.assertNotEqual(self.user.password, 'password123')
        self.assertNotEqual(user2.password, 'password123')
        self.assertNotEqual(self.user.password, user2.password)


if __name__ == '__main__':
    unittest.main()
