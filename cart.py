class ShoppingCart:
    
    def __init__(self):
        self.items = {}
    
    def add_item(self, appliance):
        appliance_id = appliance["id"]
        if appliance_id in self.items:
            self.items[appliance_id]["quantity"] += 1
        else:
            self.items[appliance_id] = {
                "appliance": appliance,
                "quantity": 1
            }
    
    def remove_item(self, appliance_id):
        if appliance_id in self.items:
            del self.items[appliance_id]
            return True
        return False
    
    def get_total(self, membership_package=None):
        total = 0
        for item in self.items.values():
            price = item["appliance"]["price"]
            quantity = item["quantity"]
            
            if membership_package:
                price = Membership.calculate_discount(price, membership_package)
            
            total += price * quantity
        return total
    
    def get_item_count(self):
        return sum(item["quantity"] for item in self.items.values())
    
    def clear(self):
        self.items.clear()
    
    def is_empty(self):
        return len(self.items) == 0
    
    def display(self, membership_package=None):
        print("\n" + "=" * 70)
        print("SHOPPING CART")
        print("=" * 70)
        
        if self.is_empty():
            print("\nYour cart is empty")
            return
        
        print(f"\n{'Product':<30} {'Qty':>5} {'Price':>15} {'Subtotal':>15}")
        print("-" * 70)
        
        total = 0
        for item in self.items.values():
            appliance = item["appliance"]
            quantity = item["quantity"]
            price = appliance["price"]
            
            if membership_package:
                price = Membership.calculate_discount(price, membership_package)
            
            subtotal = price * quantity
            total += subtotal
            
            print(f"{appliance['name']:<30} {quantity:>5} "
                  f"{self._format_price(price):>15} "
                  f"{self._format_price(subtotal):>15}")
        
        if membership_package:
            package_info = Membership.get_package_info(membership_package)
            print("-" * 70)
            print(f"Membership: {membership_package} ({package_info['discount']}% discount)")
        
        print("-" * 70)
        print(f"{'TOTAL':<30} {self.get_item_count():>5} items "
              f"{' '*15} {self._format_price(total):>15}")
    
    def _format_price(self, price):
        return f"{price:,.0f} UZS"
