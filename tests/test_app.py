"""Integration tests for Flask application"""
import unittest
import os
import tempfile
from passify import create_app


class FlaskAppTestCase(unittest.TestCase):
    """Test the Flask application routes and functionality"""
    
    def setUp(self):
        """Set up test client and environment"""
        # Configure app for testing
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create test client
        self.client = self.app.test_client()
        
        # Create a temporary history file path
        self.test_history_file = os.path.join(tempfile.gettempdir(), 'test_history.txt')
        # Patch the HISTORY_FILE path
        self.history_patcher = unittest.mock.patch(
            'passify.utils.constants.HISTORY_FILE', 
            self.test_history_file
        )
        self.history_patcher.start()
        
    def tearDown(self):
        """Clean up after tests"""
        # Remove test history file
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
        self.history_patcher.stop()
        
    def test_index_page_get(self):
        """Test index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password Generator', response.data)
        
    def test_generate_password(self):
        """Test password generation via form submission"""
        response = self.client.post('/', data={
            'length': 16,
            'use_upper': 'on',
            'use_lower': 'on',
            'use_digits': 'on',
            'min_upper': 2,
            'min_lower': 2,
            'min_digits': 2
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Check that we have a password displayed
        self.assertIn(b'Your Password:', response.data)
        
    def test_invalid_generation(self):
        """Test form validation for invalid settings"""
        # Try to generate with no character types
        response = self.client.post('/', data={
            'length': 8,
            # No character types selected
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'At least one character type must be selected', response.data)
        
    def test_history_page(self):
        """Test history page displays correctly"""
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password History', response.data)
        
    def test_export_history_empty(self):
        """Test exporting when history is empty"""
        response = self.client.get('/export')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'No history to export')
        
    def test_export_history_with_content(self):
        """Test exporting with history content"""
        # Create a history file with content
        with open(self.test_history_file, 'w') as f:
            f.write("2023-01-01 12:00:00 UTC | TestPassword123!")
        
        response = self.client.get('/export')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Disposition'], 
                         'attachment; filename=password_history.txt')
        self.assertIn(b'TestPassword123!', response.data)
        
    def test_clear_history(self):
        """Test clearing history"""
        # Create a history file with content
        with open(self.test_history_file, 'w') as f:
            f.write("2023-01-01 12:00:00 UTC | TestPassword123!")
            
        # Clear history
        response = self.client.post('/clear', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify file exists but is empty
        self.assertTrue(os.path.exists(self.test_history_file))
        with open(self.test_history_file, 'r') as f:
            content = f.read()
            self.assertEqual(content, "")


if __name__ == '__main__':
    unittest.main()