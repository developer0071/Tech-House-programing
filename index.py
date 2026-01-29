import os
import time
from cart import ShoppingCart
from membership import Membership
from database import Database
from auth import AuthSystem


class TechHouseApp:
    DELIVERY_FEE = 50000
    
    def __init__(self):
        self.database = Database()
        self.cart = ShoppingCart()
        self.auth = AuthSystem()
    
    def run(self):
        self._clear()
        print("WELCOME TO TECH HOUSE - Home Appliance Store")
        print("Your one-stop shop for quality home appliances!\n")
        input("Press ENTER to continue...")
        self._auth_menu()
    
    def _auth_menu(self):
        while True:
            self._clear()
            print("TECH HOUSE\n")
            print("1. Login")
            print("2. Register")
            print("3. Continue as guest")
            print("0. Exit\n")
            
            choice = input("Select: ").strip()
            
            if choice == "1":
                if self._login():
                    self._main_menu()
            elif choice == "2":
                self._register()
            elif choice == "3":
                print("\nEntering as guest...")
                time.sleep(1)
                self._main_menu()
            elif choice == "0":
                self._exit()
                break
            else:
                print("\nInvalid choice!")
                time.sleep(1)
    
    def _login(self):
        self._clear()
        print("LOGIN\n")
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, msg = self.auth.login(username, password)
        print(f"\n{msg}")
        time.sleep(1.5)
        return success
    
    def _register(self):
        self._clear()
        print("REGISTER\n")
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        
        if password != confirm_password:
            print("\nPasswords do not match!")
            time.sleep(1.5)
            return
        
        success, msg = self.auth.register(username, password)
        print(f"\n{msg}")
        
        if success:
            print("You can now login with your credentials.")
        
        time.sleep(2)
    
    def _main_menu(self):
        menu_actions = {
            "1": self._view_by_category,
            "2": self._search_products,
            "3": self._view_membership,   
            "4": self._add_to_cart,
            "5": self._view_cart,
            "6": self._checkout,
            "7": self._check_admin_status,
            "8": self._view_purchase_history,
            "9": self._set_delivery_address,
            "10": self._add_product,
            "11": self._make_admin,
        }
        
        while True:
            self._clear()
            self._show_main_header()
            choice = input("\nSelect: ").strip()
            
            if choice == "0":
                self.auth.logout()
                print("\nReturning to main menu...")
                time.sleep(1)
                break
            elif choice == "99":
                self._exit_app()
                return
            elif choice in menu_actions:
                menu_actions[choice]()
            else:
                print("\nInvalid choice!")
                time.sleep(1)
    
    def _show_main_header(self):
        print("MAIN MENU\n")
        
        user = self.auth.get_current_user()
        if user:
            print(f"Logged in as: {user['username']} ({user['role']})")
            if user.get('membership'):
                package = Membership.get_package_info(user['membership'])
                print(f"Membership: {user['membership']} ({package['discount']}% discount)")
            print(f"Total Purchases: {user.get('total_purchases', 0)}")
            if user.get('delivery_address'):
                address = user['delivery_address']
                if len(address) > 40:
                    address = address[:37] + "..."
                print(f"Delivery Address: {address}")
        else:
            print("Guest Mode (Login to access membership benefits)")
        
        print(f"Cart: {self.cart.get_item_count()} items\n")
        
        print("SHOPPING")
        print("1. View by category")
        print("2. Search products")
        print("3. Membership (view + set)")
        print("4. Add to cart")
        print("5. View cart")
        print("6. Checkout")

        if user:
            print("\nACCOUNT")
            print("7. Check admin status")
            print("8. View purchase history")
            print("9. Set delivery address")

            if self.auth.is_admin():
                print("\nADMIN")
                print("10. Add product")
                print("11. Make user admin")

        print("\n0. Back/Logout")
        print("99. Exit Application")
    
    def _view_by_category(self):
        self._clear()
        print("CATEGORIES\n")

        categories = self.database.get_all_categories()

        if not categories:
            print("No categories available\n")
            input("Press ENTER...")
            return

        print("0. Cancel / Back")
        print("A. View ALL products\n")

        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        choice = input("\nSelect category (number), A for all, 0 to cancel: ").strip().lower()

        if choice == "0":
            return
        elif choice == "a":
            self._view_all_products()   
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                self._show_category_products(categories[idx])
            else:
                print("\nInvalid category!")
                time.sleep(1)
        else:
            print("\nInvalid choice!")
            time.sleep(1)

        input("\nPress ENTER...")
    
    def _show_category_products(self, category):
        appliances = self.database.get_appliances_by_category(category)
        
        print(f"\n{category}\n")
        
        if not appliances:
            print("No products available in this category")
            return
        
        for app in appliances:
            print(f"ID: {app['id']:>3} | {app['name']:<30} | {self._fmt(app['price'])}")
    
    def _search_products(self):
        self._clear()
        print("SEARCH PRODUCTS\n")
        
        keyword = input("Enter keyword: ").strip()
        
        if not keyword:
            print("\nPlease enter a search term\n")
            input("Press ENTER...")
            return
        
        results = self.database.search_appliances(keyword)
        
        print(f"\nSearch results for '{keyword}':\n")
        
        if results:
            for app in results:
                print(f"ID: {app['id']:>3} | {app['name']:<30} | {self._fmt(app['price'])}")
            print(f"\nFound {len(results)} product(s)")
        else:
            print("No products found")
        
        input("\nPress ENTER...")
    
    def _view_all_products(self):
        self._clear()
        print("ALL AVAILABLE PRODUCTS\n")
        
        appliances = self.database.get_available_appliances()
        
        if not appliances:
            print("No products available\n")
            input("Press ENTER...")
            return
        
        categories = {}
        for app in appliances:
            cat = app["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(app)
        
        for category in sorted(categories.keys()):
            print(f"\n{category}\n")
            for app in categories[category]:
                print(f"ID: {app['id']:>3} | {app['name']:<30} | {self._fmt(app['price'])}")
        
        print(f"\nTotal products: {len(appliances)}")
        input("\nPress ENTER...")
    
    def _view_membership(self):
        self._clear()
        print("MEMBERSHIP CENTER\n")

        Membership.display_packages()

        user = self.auth.get_current_user()

        if not user:
            print("\nLogin to set a membership and unlock discounts!\n")
            input("Press ENTER...")
            return

        current = user.get("membership")
        purchases = user.get("total_purchases", 0)

        print("\nYOUR STATS")
        print(f"User: {user['username']}")
        print(f"Total Purchases: {purchases}")

        if current:
            info = Membership.get_package_info(current)
            free_delivery = "YES" if Membership.has_free_delivery(current) else "NO"
            print(f"\nCurrent Membership: {current}")
            print(f"Discount: {info['discount']}%")
            print(f"Free Delivery: {free_delivery}")
        else:
            print("\nCurrent Membership: None")
            print("Discount: 0%")
            print("Free Delivery: NO")

        print("\nSET / CHANGE MEMBERSHIP")
        print("1. Bronze (5% discount)")
        print("2. Silver (10% discount)")
        print("3. Gold (15% discount + Free delivery)")
        print("0. Keep current / Back")

        choice = input("\nSelect: ").strip()
        packages = {"1": "Bronze", "2": "Silver", "3": "Gold"}

        if choice == "0":
            return

        if choice in packages:
            selected = packages[choice]
            user["membership"] = selected
            self.auth.users[user["username"]]["membership"] = selected
            print(f"\nMembership successfully set to {selected}!")
        else:
            print("\nInvalid choice!")

        time.sleep(1.5)
    
    def _add_to_cart(self):
        self._clear()
        print("ADD TO CART\n")
        
        appliances = self.database.get_available_appliances()
        
        if not appliances:
            print("No products available\n")
            input("Press ENTER...")
            return
        
        for app in appliances:
            print(f"ID: {app['id']:>3} | {app['name']:<30} | {self._fmt(app['price'])}")
        
        app_id = input("\nEnter product ID (0 to cancel): ").strip()
        
        if app_id.isdigit() and app_id != "0":
            app_id = int(app_id)
            appliance = self.database.get_appliance(app_id)
            
            if appliance and appliance["status"] == "Available":
                qty_str = input("Quantity (default 1): ").strip()
                if qty_str == "":
                    qty = 1
                elif qty_str.isdigit():
                    qty = int(qty_str)
                else:
                    print("\nInvalid quantity!")
                    time.sleep(1.5)
                    return

                if qty <= 0:
                    print("\nQuantity must be at least 1!")
                    time.sleep(1.5)
                    return

                self.cart.add_item(appliance, qty)
                print(f"\nAdded {qty} x {appliance['name']} to cart!")
            else:
                print("\nInvalid product ID or product unavailable!")
        
        time.sleep(1.5)
    
    def _view_cart(self):
        self._clear()
        
        user = self.auth.get_current_user()
        membership = user.get('membership') if user else None
        
        self.cart.display(membership)
        
        if not self.cart.is_empty():
            print()
            if membership and Membership.has_free_delivery(membership):
                print("Delivery: FREE (Gold membership benefit)")
            else:
                print(f"Delivery: {self._fmt(self.DELIVERY_FEE)}")
            
            total_with_delivery = self.cart.get_total(membership)
            if not (membership and Membership.has_free_delivery(membership)):
                total_with_delivery += self.DELIVERY_FEE
            
            print(f"\nGRAND TOTAL: {self._fmt(total_with_delivery)}")
            
        while True:
            print("\nCART EDIT")
            print("1. Set quantity (replace)")
            print("2. Remove quantity (decrease)")
            print("3. Remove item")
            print("0. Done")

            c = input("Select: ").strip()
            if c == "0":
                break

            pid = input("Enter product ID: ").strip()
            if not pid.isdigit():
                print("Invalid ID!")
                continue
            pid = int(pid)

            if c == "1":
                q = input("Set quantity to: ").strip()
                if q.isdigit():
                    self.cart.set_quantity(pid, int(q))
            elif c == "2":
                q = input("Remove how many?: ").strip()
                if q.isdigit():
                    self.cart.remove_quantity(pid, int(q))
            elif c == "3":
                self.cart.remove_item(pid)

        input("\nPress ENTER...")
    
    def _checkout(self):
        if self.cart.is_empty():
            print("\nYour cart is empty!")
            time.sleep(1)
            return
        
        user = self.auth.get_current_user()
        membership = user.get('membership') if user else None
        
        self._clear()
        print("FULFILLMENT METHOD\n")
        print("1. Store Pickup (Free)")
        print("2. Home Delivery")
        
        fulfillment_choice = input("\nSelect (1-2): ").strip()
        is_delivery = fulfillment_choice == "2"
        
        delivery_address = "STORE PICKUP"
        current_delivery_fee = 0

        if is_delivery:
            current_delivery_fee = 0 if (membership and Membership.has_free_delivery(membership)) else self.DELIVERY_FEE
            
            delivery_address = user.get('delivery_address') if user else None
            if not delivery_address:
                print("\nPLEASE ENTER YOUR DELIVERY ADDRESS:")
                street = input("Street/Building: ").strip()
                district = input("District: ").strip()
                city = input("City: ").strip()
                
                if not street or not city:
                    print("\nAddress incomplete! Checkout cancelled.")
                    time.sleep(2)
                    return
                
                delivery_address = f"{street}, {district}, {city}"
                
                if user:
                    save = input("\nSave this address for future orders? (yes/no): ").strip().lower()
                    if save == "yes" or save == "y":
                        self.auth.set_delivery_address(user['username'], delivery_address)

        from datetime import datetime, timedelta
        now = datetime.now()
        
        if not is_delivery:
            delivery_msg = "Ready for pickup in: 2 hours"
        elif membership == "Gold":
            delivery_time = now + timedelta(hours=5)
            delivery_msg = f"Express Delivery by: {delivery_time.strftime('%H:%M Today')}"
        elif membership == "Silver":
            delivery_time = now + timedelta(days=1)
            delivery_msg = f"Standard Delivery by: {delivery_time.strftime('%Y-%m-%d %H:%M')}"
        else:
            delivery_time = now + timedelta(days=3)
            delivery_msg = f"Economy Delivery by: {delivery_time.strftime('%Y-%m-%d %H:%M')}"

        self._clear()
        print("CHECKOUT SUMMARY\n")
        
        self.cart.display(membership)
        
        discounted_subtotal = self.cart.get_total(membership)
        final_total = discounted_subtotal + current_delivery_fee
        
        print(f"\nMethod: {'Delivery' if is_delivery else 'Store Pickup'}")
        print(f"Schedule: {delivery_msg}")
        print(f"Fee: {self._fmt(current_delivery_fee) if current_delivery_fee > 0 else 'FREE'}\n")
        
        original_subtotal = self.cart.get_total(None)
        savings = original_subtotal - discounted_subtotal
        if savings > 0:
            print(f"Subtotal (before discount): {self._fmt(original_subtotal)}")
            print(f"Subtotal (after discount):  {self._fmt(discounted_subtotal)}")
            print(f"You save:                 {self._fmt(savings)}")
        else:
            print(f"Subtotal: {self._fmt(discounted_subtotal)}")
        print(f"TOTAL TO PAY: {self._fmt(final_total)}\n")
        
        confirm = input("Confirm purchase? (yes/no): ").strip().lower()
        
        if confirm == "yes" or confirm == "y":
            purchase_items = []
            for item in self.cart.get_items().values():
                appliance = item["appliance"]
                purchase_items.append({
                    "name": appliance["name"],
                    "quantity": item["quantity"],
                    "unit_price": appliance["price"],
                    "total_price": appliance["price"] * item["quantity"]
                })
                self.database.update_appliance_status(appliance["id"], "Sold")
            
            username = user['username'] if user else "Guest"
            self.database.add_sale(
                username=username,
                items=purchase_items,
                total_amount=final_total,
                delivery_address=delivery_address,
                delivery_fee=current_delivery_fee,
                date=f"{now.strftime('%Y-%m-%d %H:%M:%S')} (Est. Arrival: {delivery_msg})"
            )
            
            if user:
                self.auth.add_purchase(user['username'])
            
            print(f"\nORDER COMPLETED AT {now.strftime('%H:%M:%S')}!")
            print(f"Fulfillment: {delivery_msg}")
            self.cart.clear()
        else:
            print("\nOrder cancelled")
        
        time.sleep(3)
    
    def _check_admin_status(self):
        user = self.auth.get_current_user()
        if not user:
            print("\nPlease login first!")
            time.sleep(1)
            return
        
        self._clear()
        print("ADMIN STATUS\n")
        
        print(f"Username: {user['username']}")
        print(f"Current Role: {user['role']}")
        print(f"Total Purchases: {user.get('total_purchases', 0)}")
        
        if user["role"] == "admin":
            print("\nYou are already an admin!")
        else:
            can_upgrade, msg = self.auth.can_become_admin(user['username'])
            print(f"\nStatus: {msg}")
            
            if can_upgrade:
                print("\nYou are eligible for admin promotion!")
                print("Ask the current admin to promote you using option 11 in the main menu.")
            else:
                remaining = 5 - user.get('total_purchases', 0)
                print(f"\nComplete {remaining} more purchase(s) to become eligible.")
        
        input("\nPress ENTER...")
    
    def _view_purchase_history(self):
        user = self.auth.get_current_user()
        if not user:
            print("\nPlease login first!")
            time.sleep(1)
            return
        
        self._clear()
        print("PURCHASE HISTORY\n")
        
        purchases = self.database.get_user_purchases(user['username'])
        
        if not purchases:
            print("You haven't made any purchases yet.")
            print("Start shopping to build your purchase history!\n")
            input("Press ENTER...")
            return
        
        print(f"Total Orders: {len(purchases)}\n")
        
        for i, sale in enumerate(purchases, 1):
            print(f"Order #{sale['id']} - {sale['date']}\n")
            
            print(f"{'Item':<30} {'Qty':>5} {'Unit Price':>15} {'Total':>15}")
            
            for item in sale['items']:
                print(f"{item['name']:<30} {item['quantity']:>5} "
                      f"{self._fmt(item['unit_price']):>15} "
                      f"{self._fmt(item['total_price']):>15}")
            
            print(f"\nDelivery Fee: {self._fmt(sale['delivery_fee']) if sale['delivery_fee'] > 0 else 'FREE'}")
            print(f"Total Amount: {self._fmt(sale['total_amount'])}")
            print(f"Delivered to: {sale['delivery_address']}")
            
            if i < len(purchases):
                print()
        
        input("\nPress ENTER...")
    
    def _set_delivery_address(self):
        user = self.auth.get_current_user()
        if not user:
            print("\nPlease login first!")
            time.sleep(1)
            return
        
        self._clear()
        print("DELIVERY ADDRESS\n")
        
        current_address = user.get('delivery_address')
        if current_address:
            print(f"Current Address: {current_address}")
            update = input("\nUpdate address? (yes/no): ").strip().lower()
            if update != "yes" and update != "y":
                return
        
        print("\nEnter your delivery address:")
        street = input("Street/Building: ").strip()
        district = input("District: ").strip()
        city = input("City: ").strip()
        postal = input("Postal Code (optional): ").strip()
        phone = input("Phone Number: ").strip()
        
        if not street or not city:
            print("\nStreet and City are required!")
            time.sleep(1.5)
            return
        
        address_parts = [street]
        if district:
            address_parts.append(district)
        address_parts.append(city)
        if postal:
            address_parts.append(postal)
        if phone:
            address_parts.append(f"Tel: {phone}")
        
        full_address = ", ".join(address_parts)
        
        self.auth.set_delivery_address(user['username'], full_address)
        
        print("\nDelivery address saved successfully!")
        print(f"\n{full_address}")
        time.sleep(2)
    
    def _add_product(self):
        if not self.auth.is_admin():
            print("\nAdmin access required!")
            time.sleep(1)
            return
        
        self._clear()
        print("[ADMIN] ADD PRODUCT\n")
        
        name = input("Product name: ").strip()
        price_str = input("Price (UZS): ").strip()
        
        if not name:
            print("\nProduct name cannot be empty!")
            time.sleep(1)
            return
        
        if not price_str.isdigit():
            print("\nInvalid price!")
            time.sleep(1)
            return
        
        price = int(price_str)
        if price <= 0:
            print("\nPrice must be greater than 0!")
            time.sleep(1)
            return
        
        categories = self.database.get_all_categories()
        print("\nSelect category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Create new category")
        
        cat_choice = input("\nSelect: ").strip()
        
        if not cat_choice.isdigit():
            print("\nInvalid choice!")
            time.sleep(1)
            return
        
        cat_idx = int(cat_choice) - 1
        
        if cat_idx == len(categories):
            category = input("Enter new category name: ").strip()
            if not category:
                print("\nCategory name cannot be empty!")
                time.sleep(1)
                return
        elif 0 <= cat_idx < len(categories):
            category = categories[cat_idx]
        else:
            print("\nInvalid choice!")
            time.sleep(1)
            return
        
        app_id = self.database.add_appliance(name, price, "Available", category)
        print(f"\nProduct added successfully!")
        print(f"Product ID: {app_id}")
        print(f"Name: {name}")
        print(f"Price: {self._fmt(price)}")
        print(f"Category: {category}")
        
        time.sleep(3)
    
    def _make_admin(self):
        if not self.auth.is_admin():
            print("\nAdmin access required!")
            time.sleep(1)
            return
        
        self._clear()
        print("[ADMIN] MAKE USER ADMIN\n")
        
        print("Registered Users:\n")
        
        users = self.auth.get_all_users()
        eligible_users = []
        
        for username, user in users.items():
            if username != "admin":
                purchases = user.get('total_purchases', 0)
                status = "Eligible" if purchases >= 5 else f"{5-purchases} more needed"
                if user['role'] != 'admin':
                    print(f"{username:<20} | Purchases: {purchases} | {status}")
                    if purchases >= 5:
                        eligible_users.append(username)
                else:
                    print(f"{username:<20} | Already Admin")
        
        if not eligible_users:
            print("\nNo eligible users for promotion\n")
            input("Press ENTER...")
            return
        
        print(f"\nEligible users: {', '.join(eligible_users)}")
        
        username = input("\nEnter username to promote: ").strip()
        
        if username not in users:
            print("\nUser not found!")
            time.sleep(1)
            return
        
        password = input("Enter admin password: ").strip()
        
        success, msg = self.auth.make_admin(username, password)
        
        print(f"\n{msg}")
        time.sleep(2)
    
    def _exit_app(self):
        self._clear()
        print("THANK YOU FOR VISITING TECH HOUSE!")
        print("We hope to see you again soon!")
        time.sleep(2)
        exit(0)
    
    def _exit(self):
        self._clear()
        print("LOGGING OUT")
        time.sleep(1)
    
    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
    
    def _fmt(self, price):
        return f"{int(price):,} UZS"


if __name__ == "__main__":
    app = TechHouseApp()
    app.run()