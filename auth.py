import hashlib
from datetime import datetime


class AuthSystem:
    """Authentication system for managing users and roles"""
    
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.users["admin"] = {
            "username": "admin",
            "password": self._hash_password("admin123"),
            "role": "admin",
            "membership": None,
            "total_purchases": 0
        }
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
        """Register a new user"""
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if username in self.users:
            return False, "Username already exists"
        
        if len(password) < 3:
            return False, "Password must be at least 3 characters"
        
        self.users[username] = {
            "username": username,
            "password": self._hash_password(password),
            "role": "customer",
            "membership": None,
            "total_purchases": 0,
            "delivery_address": None
        }
        return True, "Registration successful"
    
    def login(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if username not in self.users:
            return False, "Invalid username or password"
        
        user = self.users[username]
        if user["password"] != self._hash_password(password):
            return False, "Invalid username or password"
        
        self.current_user = user
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        if self.current_user:
            username = self.current_user["username"]
            self.current_user = None
            return True, f"Goodbye, {username}!"
        return False, "No user logged in"
    
    def is_admin(self):
        return self.current_user and self.current_user.get("role") == "admin"
    
    def is_logged_in(self):
        return self.current_user is not None
    
    def get_current_user(self):
        return self.current_user
    
    def add_purchase(self, username):
        if username in self.users:
            if "total_purchases" not in self.users[username]:
                self.users[username]["total_purchases"] = 0
            self.users[username]["total_purchases"] += 1
            
            if self.current_user and self.current_user["username"] == username:
                self.current_user["total_purchases"] = self.users[username]["total_purchases"]
            return True
        return False
    
    def can_become_admin(self, username):
        if username not in self.users:
            return False, "User not found"
        
        user = self.users[username]
        
        if user.get("role") == "admin":
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
        
        if username == "admin":
            return False, "Cannot modify default admin account"
        
        user = self.users[username]
        
        if user.get("role") == "admin":
            return False, "User is already an admin"
        
        total_purchases = user.get("total_purchases", 0)
        if total_purchases < 5:
            return False, f"User needs at least 5 purchases (currently has {total_purchases})"
        
        user["role"] = "admin"
        
        if self.current_user and self.current_user["username"] == username:
            self.current_user["role"] = "admin"
        
        return True, f"Successfully promoted {username} to admin"
    
    def get_all_users(self):
        """Get all users (for admin view)"""
        return {username: user for username, user in self.users.items()}
    
    def set_delivery_address(self, username, address):
        """Set delivery address for user"""
        if username in self.users:
            self.users[username]["delivery_address"] = address
            if self.current_user and self.current_user["username"] == username:
                self.current_user["delivery_address"] = address
            return True
        return False
    
    def get_delivery_address(self, username):
        if username in self.users:
            return self.users[username].get("delivery_address")
        return None