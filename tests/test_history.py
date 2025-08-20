"""Unit tests for password history functionality"""
import os
import unittest
import tempfile
from unittest.mock import patch, mock_open
from passify.models.history import PasswordHistory
from passify.utils.constants import MAX_HISTORY


class TestPasswordHistory(unittest.TestCase):
    """Test password history storage and retrieval"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary test file path
        self.test_history_file = os.path.join(tempfile.gettempdir(), 'test_history.txt')
        # Patch the HISTORY_FILE constant
        self.patcher = patch('passify.models.history.HISTORY_FILE', self.test_history_file)
        self.mock_history_file = self.patcher.start()
        
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove the test file if it exists
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
        self.patcher.stop()
        
    def test_save_new_entry(self):
        """Test saving when history file doesn't exist"""
        # Ensure file doesn't exist
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
            
        # Save a password
        test_password = "TestPassword123!"
        PasswordHistory.save(test_password)
        
        # Check if file was created and contains the password
        self.assertTrue(os.path.exists(self.test_history_file))
        with open(self.test_history_file, 'r') as f:
            content = f.read()
            self.assertIn(test_password, content)
            
    def test_append_entry(self):
        """Test appending entries to existing history"""
        # Create file with one entry
        with open(self.test_history_file, 'w') as f:
            f.write("2023-01-01 12:00:00 UTC | Password1\n")
            
        # Add a new entry
        PasswordHistory.save("Password2")
        
        # Check if both entries exist
        with open(self.test_history_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("Password1", lines[0])
            self.assertIn("Password2", lines[1])
            
    def test_max_history_limit(self):
        """Test that history size is limited to MAX_HISTORY"""
        # Create a file with MAX_HISTORY+10 entries
        with open(self.test_history_file, 'w') as f:
            for i in range(MAX_HISTORY + 10):
                f.write(f"2023-01-01 12:00:00 UTC | Password{i}\n")
                
        # Add one more entry
        PasswordHistory.save("FinalPassword")
        
        # Verify that only MAX_HISTORY entries are kept
        with open(self.test_history_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), MAX_HISTORY)
            # Check the last entry is our new one
            self.assertIn("FinalPassword", lines[-1])
            # The first entries should be removed
            for i in range(10):
                self.assertNotIn(f"Password{i}", "".join(lines))
                
    def test_get_all_empty(self):
        """Test getting history when empty"""
        # Ensure file doesn't exist
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
            
        history = PasswordHistory.get_all()
        self.assertEqual(history, [])
        
    def test_get_all_with_entries(self):
        """Test getting history with entries"""
        # Create file with entries
        with open(self.test_history_file, 'w') as f:
            f.write("2023-01-01 12:00:00 UTC | Password1\n")
            f.write("2023-01-02 12:00:00 UTC | Password2\n")
            
        history = PasswordHistory.get_all()
        self.assertEqual(len(history), 2)
        # Check that newest is first (reverse order)
        self.assertIn("Password2", history[0])
        self.assertIn("Password1", history[1])
        
    def test_clear_history(self):
        """Test clearing history"""
        # Create file with entries
        with open(self.test_history_file, 'w') as f:
            f.write("2023-01-01 12:00:00 UTC | Password1\n")
            
        # Clear history
        PasswordHistory.clear()
        
        # Verify file exists but is empty
        self.assertTrue(os.path.exists(self.test_history_file))
        with open(self.test_history_file, 'r') as f:
            content = f.read()
            self.assertEqual(content, "")
            
    def test_export(self):
        """Test exporting history"""
        # Create file with entries
        test_content = "2023-01-01 12:00:00 UTC | Password1\n"
        with open(self.test_history_file, 'w') as f:
            f.write(test_content)
            
        exported = PasswordHistory.export()
        self.assertEqual(exported, test_content)
        
        # Test export with no file
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
        exported = PasswordHistory.export()
        self.assertEqual(exported, "")


if __name__ == '__main__':
    unittest.main()