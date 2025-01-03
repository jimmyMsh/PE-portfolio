import unittest
from unittest.mock import patch
from app import app, TimelinePost

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test"""
        TimelinePost.delete().execute()

    def test_login_workflow(self):
        """Test the complete login workflow"""
        # Test login with correct password
        response = self.client.post('/api/admin/login', data={
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Login successful')

        # Verify we can access protected endpoint after login
        post = TimelinePost.create(
            name='Test', 
            email='test@example.com',
            content='Test content'
        )
        delete_response = self.client.delete(f'/api/timeline_post/{post.id}')
        self.assertEqual(delete_response.status_code, 200)

        # Test logout
        logout_response = self.client.post('/api/admin/logout')
        self.assertEqual(logout_response.status_code, 200)

        # Verify we can't access protected endpoint after logout
        post2 = TimelinePost.create(
            name='Test2', 
            email='test2@example.com',
            content='Test content 2'
        )
        delete_response = self.client.delete(f'/api/timeline_post/{post2.id}')
        self.assertEqual(delete_response.status_code, 401)

    def test_failed_login(self):
        """Test login failures"""
        # Test wrong password
        response = self.client.post('/api/admin/login', data={
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Invalid password')

        # Test missing password
        response = self.client.post('/api/admin/login', data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Password is required')

    def test_protected_routes(self):
        """Test protected route access"""
        # Create a post to delete
        post = TimelinePost.create(
            name='Test', 
            email='test@example.com',
            content='Test content'
        )

        # Try to delete without login
        response = self.client.delete(f'/api/timeline_post/{post.id}')
        self.assertEqual(response.status_code, 401)