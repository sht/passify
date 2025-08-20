"""Unit tests for password generator functionality"""
import unittest
from passify.core.password_generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Test password generator core functions"""
    
    def test_default_settings(self):
        """Test generator with default settings"""
        generator = PasswordGenerator()
        password = generator.generate()
        
        # Check length
        self.assertEqual(len(password), 14)
        
        # Check character types present
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        
    def test_custom_length(self):
        """Test password with custom length"""
        generator = PasswordGenerator(length=20)
        password = generator.generate()
        self.assertEqual(len(password), 20)
        
    def test_character_options(self):
        """Test password with specific character options"""
        # Only uppercase
        gen_upper = PasswordGenerator(
            use_upper=True, 
            use_lower=False,
            use_digits=False, 
            use_special=False,
            min_upper=1
        )
        pwd_upper = gen_upper.generate()
        self.assertEqual(len(pwd_upper), 14)
        self.assertTrue(all(c.isupper() for c in pwd_upper))
        
        # Only lowercase
        gen_lower = PasswordGenerator(
            use_upper=False, 
            use_lower=True,
            use_digits=False, 
            use_special=False,
            min_lower=1
        )
        pwd_lower = gen_lower.generate()
        self.assertEqual(len(pwd_lower), 14)
        self.assertTrue(all(c.islower() for c in pwd_lower))
        
        # Only digits
        gen_digits = PasswordGenerator(
            use_upper=False, 
            use_lower=False,
            use_digits=True, 
            use_special=False,
            min_digits=1
        )
        pwd_digits = gen_digits.generate()
        self.assertEqual(len(pwd_digits), 14)
        self.assertTrue(all(c.isdigit() for c in pwd_digits))
        
    def test_minimum_requirements(self):
        """Test minimum character requirements"""
        generator = PasswordGenerator(
            length=10,
            use_upper=True, 
            use_lower=True,
            use_digits=True, 
            use_special=False,
            min_upper=3,
            min_lower=3,
            min_digits=4
        )
        password = generator.generate()
        
        # Check password length
        self.assertEqual(len(password), 10)
        
        # Count character types
        upper_count = sum(1 for c in password if c.isupper())
        lower_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        
        # Verify minimums
        self.assertGreaterEqual(upper_count, 3)
        self.assertGreaterEqual(lower_count, 3)
        self.assertGreaterEqual(digit_count, 4)
        
    def test_validation_errors(self):
        """Test validation error scenarios"""
        # No character types selected
        with self.assertRaises(ValueError):
            generator = PasswordGenerator(
                use_upper=False, 
                use_lower=False,
                use_digits=False, 
                use_special=False
            )
            generator.generate()
            
        # Length too short for minimums
        with self.assertRaises(ValueError):
            generator = PasswordGenerator(
                length=5,
                min_upper=2,
                min_lower=2,
                min_digits=2
            )
            generator.generate()
            

if __name__ == '__main__':
    unittest.main()