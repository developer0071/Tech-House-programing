class Database:
    
    def __init__(self):
        self.appliances = {}
        self.customers = {}
        self.sales = {}
        self.next_appliance_id = 1
        self.next_customer_id = 1
        self.next_sale_id = 1
        self._initialize_data()
    
    def _initialize_data(self):
        # Kitchen appliances
        self.add_appliance("Mixer", 450000, "Available", "Kitchen appliances")
        self.add_appliance("Oven", 2500000, "Available", "Kitchen appliances")
        self.add_appliance("Blender", 350000, "Available", "Kitchen appliances")
        self.add_appliance("Microwave", 800000, "Available", "Kitchen appliances")
        self.add_appliance("Refrigerator", 3500000, "Available", "Kitchen appliances")
        
        # Cleaning devices
        self.add_appliance("Vacuum Cleaner", 1200000, "Available", "Cleaning devices")
        self.add_appliance("Robot Vacuum", 2800000, "Available", "Cleaning devices")
        
        # Heating and cooling
        self.add_appliance("Air Conditioner", 4500000, "Available", "Heating and cooling devices")
        self.add_appliance("Heater", 650000, "Available", "Heating and cooling devices")
        self.add_appliance("Fan", 280000, "Available", "Heating and cooling devices")
        
        # Personal care
        self.add_appliance("Hair Dryer", 180000, "Available", "Personal care devices")
        self.add_appliance("Electric Shaver", 320000, "Available", "Personal care devices")
        
        # Smart home
        self.add_appliance("Smart Speaker", 550000, "Available", "Smart home devices")
        self.add_appliance("Smart Doorbell", 780000, "Available", "Smart home devices")
        self.add_appliance("Smart Thermostat", 920000, "Available", "Smart home devices")
    
    def add_appliance(self, name, price, status, category):
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
    
    def add_customer(self, name, address, purchased_appliances):
        customer_id = self.next_customer_id
        self.customers[customer_id] = {
            "id": customer_id,
            "name": name,
            "address": address,
            "purchased_appliances": purchased_appliances
        }
        self.next_customer_id += 1
        return customer_id
    
    def add_sale(self, appliance_name, customer_id, date):
        sale_id = self.next_sale_id
        self.sales[sale_id] = {
            "id": sale_id,
            "appliance_name": appliance_name,
            "customer_id": customer_id,
            "date": date
        }
        self.next_sale_id += 1
        return sale_id
    
    def get_appliances_by_category(self, category):
        return [app for app in self.appliances.values() if app["category"] == category]
    
    def get_available_appliances(self):
        return [app for app in self.appliances.values() if app["status"] == "Available"]
    
    def search_appliances(self, keyword):
        keyword = keyword.lower()
        return [app for app in self.appliances.values() 
                if keyword in app["name"].lower() or keyword in app["category"].lower()]
    
    def update_appliance_status(self, appliance_id, status):
        if appliance_id in self.appliances:
            self.appliances[appliance_id]["status"] = status
            return True
        return False
    
    def get_customer_purchase_history(self, customer_id):
        return [sale for sale in self.sales.values() if sale["customer_id"] == customer_id]
    
    def get_all_categories(self):
        categories = set()
        for app in self.appliances.values():
            categories.add(app["category"])
        return sorted(list(categories))
