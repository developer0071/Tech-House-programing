from datetime import datetime


class Database:
    """Database for managing appliances, customers, and sales"""
    
    def __init__(self):
        self.appliances = {}
        self.customers = {}
        self.sales = {}
        self.next_appliance_id = 1
        self.next_customer_id = 1
        self.next_sale_id = 1
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize the database with sample appliances"""
        # Kitchen appliances
        self.add_appliance("Mixer", 450000, "Available", "Kitchen appliances")
        self.add_appliance("Oven", 2500000, "Available", "Kitchen appliances")
        self.add_appliance("Blender", 350000, "Available", "Kitchen appliances")
        self.add_appliance("Microwave", 800000, "Available", "Kitchen appliances")
        self.add_appliance("Refrigerator", 3500000, "Available", "Kitchen appliances")
        self.add_appliance("Toaster", 180000, "Available", "Kitchen appliances")
        self.add_appliance("Coffee Maker", 550000, "Available", "Kitchen appliances")
        
        # Cleaning devices
        self.add_appliance("Vacuum Cleaner", 1200000, "Available", "Cleaning devices")
        self.add_appliance("Robot Vacuum", 2800000, "Available", "Cleaning devices")
        self.add_appliance("Steam Cleaner", 980000, "Available", "Cleaning devices")
        
        # Heating and cooling
        self.add_appliance("Air Conditioner", 4500000, "Available", "Heating and cooling devices")
        self.add_appliance("Heater", 650000, "Available", "Heating and cooling devices")
        self.add_appliance("Fan", 280000, "Available", "Heating and cooling devices")
        self.add_appliance("Humidifier", 420000, "Available", "Heating and cooling devices")
        
        # Personal care
        self.add_appliance("Hair Dryer", 180000, "Available", "Personal care devices")
        self.add_appliance("Electric Shaver", 320000, "Available", "Personal care devices")
        self.add_appliance("Electric Toothbrush", 250000, "Available", "Personal care devices")
        
        # Smart home
        self.add_appliance("Smart Speaker", 550000, "Available", "Smart home devices")
        self.add_appliance("Smart Doorbell", 780000, "Available", "Smart home devices")
        self.add_appliance("Smart Thermostat", 920000, "Available", "Smart home devices")
        self.add_appliance("Smart Light Bulbs", 150000, "Available", "Smart home devices")
    
    def add_appliance(self, name, price, status, category):
        """Add a new appliance to the database"""
        if not name or price <= 0:
            return None
        
        appliance_id = self.next_appliance_id
        self.appliances[appliance_id] = {
            "id": appliance_id,
            "name": name,
            "price": price,
            "status": status,
            "category": category
        }
        self.next_appliance_id += 1
        return appliance_id
    
    def get_appliance(self, appliance_id):
        """Get appliance by ID"""
        return self.appliances.get(appliance_id)
    
    def add_customer(self, name, address, purchased_appliances):
        """Add a new customer"""
        customer_id = self.next_customer_id
        self.customers[customer_id] = {
            "id": customer_id,
            "name": name,
            "address": address,
            "purchased_appliances": purchased_appliances
        }
        self.next_customer_id += 1
        return customer_id
    
    def add_sale(self, username, items, total_amount, delivery_address, delivery_fee, date):
        """Record a sale"""
        sale_id = self.next_sale_id
        self.sales[sale_id] = {
            "id": sale_id,
            "username": username,
            "items": items,  # List of {appliance_name, quantity, price}
            "total_amount": total_amount,
            "delivery_address": delivery_address,
            "delivery_fee": delivery_fee,
            "date": date
        }
        self.next_sale_id += 1
        return sale_id
    
    def get_user_purchases(self, username):
        """Get all purchases for a specific user"""
        return [sale for sale in self.sales.values() 
                if sale.get("username") == username]
    
    def get_appliances_by_category(self, category):
        """Get all appliances in a specific category"""
        return [app for app in self.appliances.values() 
                if app["category"] == category and app["status"] == "Available"]
    
    def get_available_appliances(self):
        """Get all available appliances"""
        return [app for app in self.appliances.values() 
                if app["status"] == "Available"]
    
    def get_all_appliances(self):
        """Get all appliances regardless of status"""
        return list(self.appliances.values())
    
    def search_appliances(self, keyword):
        """Search appliances by keyword in name or category"""
        if not keyword:
            return []
        
        keyword = keyword.lower()
        return [app for app in self.appliances.values() 
                if (keyword in app["name"].lower() or 
                    keyword in app["category"].lower()) and 
                    app["status"] == "Available"]
    
    def update_appliance_status(self, appliance_id, status):
        """Update appliance status"""
        if appliance_id in self.appliances:
            self.appliances[appliance_id]["status"] = status
            return True
        return False
    
    def update_appliance(self, appliance_id, name=None, price=None, category=None):
        """Update appliance details"""
        if appliance_id not in self.appliances:
            return False
        
        if name:
            self.appliances[appliance_id]["name"] = name
        if price and price > 0:
            self.appliances[appliance_id]["price"] = price
        if category:
            self.appliances[appliance_id]["category"] = category
        
        return True
    
    def delete_appliance(self, appliance_id):
        """Delete an appliance"""
        if appliance_id in self.appliances:
            del self.appliances[appliance_id]
            return True
        return False
    
    def get_customer_purchase_history(self, customer_id):
        """Get purchase history for a customer"""
        return [sale for sale in self.sales.values() 
                if sale["customer_id"] == customer_id]
    
    def get_all_categories(self):
        """Get list of all unique categories"""
        categories = set()
        for app in self.appliances.values():
            categories.add(app["category"])
        return sorted(list(categories))
    
    def get_sales_stats(self):
        """Get sales statistics"""
        total_sales = len(self.sales)
        sold_items = [app for app in self.appliances.values() 
                      if app["status"] == "Sold"]
        available_items = [app for app in self.appliances.values() 
                          if app["status"] == "Available"]
        
        return {
            "total_sales": total_sales,
            "sold_items": len(sold_items),
            "available_items": len(available_items),
            "total_items": len(self.appliances)
        }