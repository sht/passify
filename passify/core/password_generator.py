"""Password generator core functionality"""
import random
import string
from passify.utils.constants import SPECIAL_CHARACTERS

class PasswordGenerator:
    """Password generation class with customizable options"""
    
    def __init__(self, **kwargs):
        """Initialize with password generation settings"""
        self.length = kwargs.get('length', 14)
        self.use_upper = kwargs.get('use_upper', True)
        self.use_lower = kwargs.get('use_lower', True)
        self.use_digits = kwargs.get('use_digits', True)
        self.use_special = kwargs.get('use_special', False)
        self.min_upper = kwargs.get('min_upper', 1)
        self.min_lower = kwargs.get('min_lower', 1)
        self.min_digits = kwargs.get('min_digits', 1)
        
    def validate_settings(self):
        """Validate the password generation settings"""
        if not (self.use_upper or self.use_lower or self.use_digits or self.use_special):
            raise ValueError("At least one character type must be selected.")

        min_required = 0
        if self.use_upper:
            min_required += self.min_upper
        if self.use_lower:
            min_required += self.min_lower
        if self.use_digits:
            min_required += self.min_digits
            
        if self.length < min_required:
            raise ValueError("Length is too short for the minimum counts specified.")
            
    def get_character_pool(self):
        """Get the pool of characters based on settings"""
        chars = ''
        if self.use_upper:
            chars += string.ascii_uppercase
        if self.use_lower:
            chars += string.ascii_lowercase
        if self.use_digits:
            chars += string.digits
        if self.use_special:
            chars += SPECIAL_CHARACTERS
        return chars
        
    def generate(self):
        """Generate a secure random password based on settings"""
        self.validate_settings()
        
        password = []
        # Add minimum required characters
        if self.use_upper:
            password += random.choices(string.ascii_uppercase, k=self.min_upper)
        if self.use_lower:
            password += random.choices(string.ascii_lowercase, k=self.min_lower)
        if self.use_digits:
            password += random.choices(string.digits, k=self.min_digits)
            
        # Fill remaining length with random characters from the pool
        chars = self.get_character_pool()
        remaining = self.length - len(password)
        if remaining > 0:
            password += random.choices(chars, k=remaining)
            
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        return ''.join(password)