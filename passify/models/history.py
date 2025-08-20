"""Password history management"""
import os
from datetime import datetime, timezone
from passify.utils.constants import HISTORY_FILE, MAX_HISTORY

class PasswordHistory:
    """Manages password history storage and retrieval"""
    
    @staticmethod
    def save(password):
        """Save password to history file"""
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        entry = f"{now} | {password}\n"
        
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                f.write(entry)
            return
        
        # Read existing history, append new entry, and limit size
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
            
        lines.append(entry)
        if len(lines) > MAX_HISTORY:
            lines = lines[-MAX_HISTORY:]
            
        with open(HISTORY_FILE, 'w') as f:
            f.writelines(lines)
    
    @staticmethod
    def get_all():
        """Get all password history entries"""
        if not os.path.exists(HISTORY_FILE):
            return []
            
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
            
        # Return newest entries first
        return [line.strip() for line in lines[::-1]]
    
    @staticmethod
    def clear():
        """Clear all history"""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                pass
                
    @staticmethod
    def export():
        """Get raw history content for export"""
        if not os.path.exists(HISTORY_FILE):
            return ""
            
        with open(HISTORY_FILE, 'r') as f:
            content = f.read()
            
        return content