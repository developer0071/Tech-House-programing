import hashlib


class AuthSystem:
    
    def __init__(self):
        self.users = {
            "admin": {
                "username": "admin",
                "password": self._hash_password("admin123"),
                "role": "admin",
                "membership": None,
                "total_purchases": 0,
                "delivery_address": None
            }
        }
        self.current_user = None
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
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
        
        user = self.users.get(username)
        if not user or user["password"] != self._hash_password(password):
            return False, "Invalid username or password"
        
        self.current_user = user
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        self.current_user = None
    
    def is_admin(self):
        return self.current_user and self.current_user["role"] == "admin"
    
    def get_current_user(self):
        return self.current_user
    
    def add_purchase(self, username):
        if username in self.users:
            self.users[username]["total_purchases"] += 1
            if self.current_user and self.current_user["username"] == username:
                self.current_user["total_purchases"] = self.users[username]["total_purchases"]
    
    def can_become_admin(self, username):
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        if user["role"] == "admin":
            return False, "Already an admin"
        
        purchases = user["total_purchases"]
        if purchases >= 5:
            return True, "Eligible for admin promotion"
        return False, f"Need {5 - purchases} more purchases to be eligible"
    
    def make_admin(self, username, admin_password):
        if self._hash_password(admin_password) != self.users["admin"]["password"]:
            return False, "Invalid admin password"
        
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        if user["role"] == "admin":
            return False, "User is already an admin"
        if user["total_purchases"] < 5:
            return False, f"User needs at least 5 purchases (currently has {user['total_purchases']})"
        
        user["role"] = "admin"
        if self.current_user and self.current_user["username"] == username:
            self.current_user["role"] = "admin"
        
        return True, f"Successfully promoted {username} to admin"
    
    def get_all_users(self):
        return self.users
    
    def set_delivery_address(self, username, address):
        if username in self.users:
            self.users[username]["delivery_address"] = address
            if self.current_user and self.current_user["username"] == username:
                self.current_user["delivery_address"] = address