"""Test command-line functionality"""
import unittest
import sys
import io
from unittest.mock import patch, MagicMock
from passify.core.password_generator import PasswordGenerator


class CommandLineTestCase(unittest.TestCase):
    """Test command-line functionality"""
    
    def test_password_generation_output(self):
        """Test that a password can be generated and correctly formatted"""
        # Create a generator with test settings
        generator = PasswordGenerator(
            length=16,
            use_upper=True,
            use_lower=True,
            use_digits=True,
            use_special=True,
            min_upper=2,
            min_lower=2,
            min_digits=2
        )
        
        # Generate a password
        password = generator.generate()
        
        # Check length
        self.assertEqual(len(password), 16)
        
        # Check minimum requirements
        upper_count = sum(1 for c in password if c.isupper())
        lower_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        
        self.assertGreaterEqual(upper_count, 2)
        self.assertGreaterEqual(lower_count, 2)
        self.assertGreaterEqual(digit_count, 2)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('passify.core.password_generator.PasswordGenerator.generate')
    def test_cli_output_format(self, mock_generate, mock_stdout):
        """Test that CLI output is correctly formatted"""
        # Mock the password generation
        mock_generate.return_value = "MockP@ssw0rd123"
        
        # Create a generator
        generator = PasswordGenerator()
        
        # Simulate printing to stdout
        print(f"Generated password: {generator.generate()}")
        
        # Check the output
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Generated password: MockP@ssw0rd123")


if __name__ == '__main__':
    unittest.main()