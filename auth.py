import hashlib
from datetime import datetime


class AuthSystem:
    
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.users["admin"] = {
            "username": "admin",
            "password": self._hash_password("admin123"),
            "role": "admin",
            "total_purchases": 0
        }
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = {
            "username": username,
            "password": self._hash_password(password),
            "role": "customer",
            "membership": None,
            "total_purchases": 0
        }
        return True, "Registration successful"
    
    def login(self, username, password):
        if username not in self.users:
            return False, "Invalid username or password"
        
        user = self.users[username]
        if user["password"] != self._hash_password(password):
            return False, "Invalid username or password"
        
        self.current_user = user
        return True, "Login successful"
    
    def logout(self):
        self.current_user = None
    
    def is_admin(self):
        return self.current_user and self.current_user["role"] == "admin"
    
    def get_current_user(self):
        """Get current user"""
        return self.current_user
    
    def add_purchase(self, username):
        if username in self.users:
            if "total_purchases" not in self.users[username]:
                self.users[username]["total_purchases"] = 0
            self.users[username]["total_purchases"] += 1
            return True
        return False
    
    def can_become_admin(self, username):
        if username not in self.users:
            return False, "User not found"
        
        user = self.users[username]
        
        if user["role"] == "admin":
            return False, "Already an admin"
        
        total_purchases = user.get("total_purchases", 0)
        
        if total_purchases >= 5:
            return True, "Eligible for admin promotion"
        else:
            return False, f"Need {5 - total_purchases} more purchases to be eligible"
    
    def make_admin(self, username, admin_password):
        if self._hash_password(admin_password) != self.users["admin"]["password"]:
            return False, "Invalid admin password"
        
        if username not in self.users:
            return False, "User not found"
        
        user = self.users[username]
        
        if user["role"] == "admin":
            return False, "User is already an admin"
        
        total_purchases = user.get("total_purchases", 0)
        if total_purchases < 5:
            return False, f"User needs at least 5 purchases (currently has {total_purchases})"
        
        user["role"] = "admin"
        return True, f"Successfully promoted {username} to admin"