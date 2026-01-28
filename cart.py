from membership import Membership


class ShoppingCart:
    """Shopping cart for managing items and calculating totals"""
    
    def __init__(self):
        self.items = {}
    
    def add_item(self, appliance):
        """Add an appliance to the cart"""
        if not appliance or "id" not in appliance:
            return False
        
        appliance_id = appliance["id"]
        if appliance_id in self.items:
            self.items[appliance_id]["quantity"] += 1
        else:
            self.items[appliance_id] = {
                "appliance": appliance.copy(),
                "quantity": 1
            }
        return True
    
    def remove_item(self, appliance_id):
        """Remove an item from cart"""
        if appliance_id in self.items:
            del self.items[appliance_id]
            return True
        return False
    
    def update_quantity(self, appliance_id, quantity):
        """Update quantity of an item"""
        if appliance_id in self.items and quantity > 0:
            self.items[appliance_id]["quantity"] = quantity
            return True
        return False
    
    def get_total(self, membership_package=None):
        """Calculate total price with optional membership discount"""
        total = 0
        for item in self.items.values():
            price = item["appliance"]["price"]
            quantity = item["quantity"]
            
            if membership_package:
                price = Membership.calculate_discount(price, membership_package)
            
            total += price * quantity
        return round(total)
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item["quantity"] for item in self.items.values())
    
    def get_unique_item_count(self):
        """Get number of unique items in cart"""
        return len(self.items)
    
    def clear(self):
        """Clear all items from cart"""
        self.items.clear()
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def get_items(self):
        """Get all items in cart"""
        return self.items.copy()
    
    def display(self, membership_package=None):
        """Display cart contents"""
        print("\n" + "=" * 70)
        print("SHOPPING CART")
        print("=" * 70)
        
        if self.is_empty():
            print("\nYour cart is empty")
            return
        
        print(f"\n{'Product':<35} {'Qty':>5} {'Price':>12} {'Subtotal':>12}")
        print("-" * 70)
        
        total = 0
        for item in self.items.values():
            appliance = item["appliance"]
            quantity = item["quantity"]
            original_price = appliance["price"]
            
            price = original_price
            discount_label = ""
            
            if membership_package:
                price = Membership.calculate_discount(original_price, membership_package)
                if price < original_price:
                    discount_pct = round((1 - price/original_price) * 100)
                    discount_label = f" (-{discount_pct}%)"
            
            subtotal = price * quantity
            total += subtotal
            
            # Truncate long names
            name = appliance['name']
            if len(name) > 30:
                name = name[:27] + "..."
            name_with_discount = name + discount_label
            
            print(f"{name_with_discount:<35} {quantity:>5} "
                  f"{self._format_price(price):>12} "
                  f"{self._format_price(subtotal):>12}")
        
        if membership_package:
            package_info = Membership.get_package_info(membership_package)
            if package_info:
                print("-" * 70)
                print(f"Membership: {membership_package} ({package_info['discount']}% discount)")
        
        print("-" * 70)
        print(f"{'TOTAL':<35} {self.get_item_count():>5} "
              f"{' '*12} {self._format_price(total):>12}")
    
    def _format_price(self, price):
        """Format price in UZS currency"""
        return f"{int(price):,} UZS"