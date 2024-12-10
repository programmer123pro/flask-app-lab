import unittest
from app import create_app, db
from app.users.models import *

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client() 
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Очищення після тестів"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        """Тестування сторінки входу"""
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_page(self):
        """Тестування сторінки реєстрації"""
        response = self.client.get('/users/sign_up/')
        self.assertEqual(response.status_code, 200)  


    def test_sign_up(self):
        """Тестування реєстрації користувача"""
        response = self.client.post('/sign_up/', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertEqual(response.status_code, 200)

    # def test_greetings_page(self):
    #     """Тест маршруту /hi/<name>."""
    #     response = self.client.get("/users/hi/John?age=30")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b"JOHN", response.data)
    #     self.assertIn(b"30", response.data)

    # def test_admin_page(self):
    #     """Тест маршруту /admin, який перенаправляє."""
    #     response = self.client.get("/users/admin", follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b"ADMINISTRATOR", response.data)
    #     self.assertIn(b"45", response.data)

if __name__ == "__main__":
    unittest.main()