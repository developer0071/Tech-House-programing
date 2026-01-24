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
        print("=" * 70)
        print("WELCOME TO TECH HOUSE - Home Appliance Store")
        print("=" * 70)
        input("\nPress ENTER to continue...")
        self._auth_menu()
    
    def _auth_menu(self):
        while True:
            self._clear()
            print("=" * 70)
            print("TECH HOUSE\n" + "=" * 70)
            print("\n1. Login\n2. Register\n3. Continue as guest\n0. Exit")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1" and self._login():
                self._main_menu()
            elif choice == "2":
                self._register()
            elif choice == "3":
                self._main_menu()
            elif choice == "0":
                self._exit()
                break
    
    def _login(self):
        self._clear()
        print("=" * 70 + "\nLOGIN\n" + "=" * 70)
        
        username = input("\nUsername: ").strip()
        password = input("Password: ").strip()
        
        success, msg = self.auth.login(username, password)
        print(f"\n{msg}")
        time.sleep(1)
        return success
    
    def _register(self):
        self._clear()
        print("=" * 70 + "\nREGISTER\n" + "=" * 70)
        
        username = input("\nUsername: ").strip()
        password = input("Password: ").strip()
        
        success, msg = self.auth.register(username, password)
        print(f"\n{msg}")
        time.sleep(1)
    
    def _main_menu(self):
        menu_actions = {
            "1": self._view_by_category,
            "2": self._search_products,
            "3": self._view_membership,
            "4": self._set_membership,
            "5": self._add_to_cart,
            "6": self._view_cart,
            "7": self._checkout,
            "8": self._check_admin_status,
            "9": self._add_product,
            "10": self._make_admin,
        }
        
        while True:
            self._clear()
            self._show_main_header()
            choice = input("\nSelect: ").strip()
            
            if choice == "0":
                self._exit()
                break
            elif choice == "99":
                if self.auth.get_current_user():
                    self.auth.logout()
                    print("\nLogged out")
                    time.sleep(1)
                    break
            elif choice in menu_actions:
                menu_actions[choice]()
    
    def _show_main_header(self):
        print("=" * 70 + "\nMAIN MENU\n" + "=" * 70)
        
        user = self.auth.get_current_user()
        if user:
            print(f"\nLogged in: {user['username']}")
            if user.get('membership'):
                print(f"Membership: {user['membership']}")
        else:
            print("\nGuest Mode")
        
        print(f"Cart: {self.cart.get_item_count()} items")
        print("\n1. View by category\n2. Search\n3. View membership")
        print("4. Set membership\n5. Add to cart\n6. View cart\n7. Checkout")
        
        if user:
            print("8. Check admin status")
            if self.auth.is_admin():
                print("9. [ADMIN] Add product\n10. [ADMIN] Make user admin")
            print("99. Logout")
        print("0. Exit")
    
    def _view_by_category(self):
        """View products by category"""
        self._clear()
        print("=" * 70 + "\nCATEGORIES\n" + "=" * 70)
        
        categories = self.database.get_all_categories()
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        choice = input("\nSelect (0 to cancel): ").strip()
        
        if choice.isdigit() and choice != "0":
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                self._show_category_products(categories[idx])
        
        input("\nPress ENTER...")
    
    def _show_category_products(self, category):
        appliances = self.database.get_appliances_by_category(category)
        print(f"\n{category}\n" + "-" * 70)
        for app in appliances:
            print(f"ID: {app['id']} | {app['name']} | {self._fmt(app['price'])}")
    
    def _search_products(self):
        self._clear()
        print("=" * 70 + "\nSEARCH\n" + "=" * 70)
        
        keyword = input("\nKeyword: ").strip()
        results = self.database.search_appliances(keyword)
        
        print(f"\nResults for '{keyword}':\n" + "-" * 70)
        
        if results:
            for app in results:
                print(f"ID: {app['id']} | {app['name']} | {self._fmt(app['price'])}")
        else:
            print("No products found")
        
        input("\nPress ENTER...")
    
    def _view_membership(self):
        self._clear()
        Membership.display_packages()
        input("\nPress ENTER...")
    
    def _set_membership(self):
        user = self.auth.get_current_user()
        if not user:
            print("\nPlease login first")
            time.sleep(1)
            return
        
        self._clear()
        print("=" * 70 + "\nSELECT MEMBERSHIP\n" + "=" * 70)
        print("\n1. Bronze (5%)\n2. Silver (10%)\n3. Gold (15% + Free delivery)\n0. Cancel")
        
        choice = input("\nSelect: ").strip()
        packages = {1: "Bronze", 2: "Silver", 3: "Gold"}
        
        if choice.isdigit() and int(choice) in packages:
            user['membership'] = packages[int(choice)]
            print(f"\nMembership set to {user['membership']}")
            time.sleep(1)
    
    def _add_to_cart(self):
        self._clear()
        print("=" * 70 + "\nADD TO CART\n" + "=" * 70)
        
        for app in self.database.get_available_appliances():
            print(f"ID: {app['id']} | {app['name']} | {self._fmt(app['price'])}")
        
        app_id = input("\nEnter ID (0 to cancel): ").strip()
        
        if app_id.isdigit() and app_id != "0":
            app_id = int(app_id)
            appliance = self.database.appliances.get(app_id)
            if appliance and appliance["status"] == "Available":
                self.cart.add_item(appliance)
                print(f"\n{appliance['name']} added")
            else:
                print("\nInvalid or unavailable")
        
        time.sleep(1)
    
    def _view_cart(self):
        self._clear()
        user = self.auth.get_current_user()
        membership = user.get('membership') if user else None
        
        self.cart.display(membership)
        
        if not self.cart.is_empty():
            print("\n" + "=" * 70)
            if membership and Membership.has_free_delivery(membership):
                print("Delivery: FREE")
            else:
                print(f"Delivery: {self._fmt(self.DELIVERY_FEE)}")
        
        input("\nPress ENTER...")
    
    def _checkout(self):
        if self.cart.is_empty():
            print("\nCart is empty")
            time.sleep(1)
            return
        
        user = self.auth.get_current_user()
        if not user:
            print("\nPlease login first")
            time.sleep(1)
            return
        
        self._clear()
        print("=" * 70 + "\nCHECKOUT\n" + "=" * 70)
        
        membership = user.get('membership')
        self.cart.display(membership)
        
        subtotal = self.cart.get_total(membership)
        delivery = 0 if (membership and Membership.has_free_delivery(membership)) else self.DELIVERY_FEE
        total = subtotal + delivery
        
        print("\n" + "=" * 70)
        print(f"Subtotal: {self._fmt(subtotal)}")
        if delivery > 0:
            print(f"Delivery: {self._fmt(delivery)}")
        print(f"TOTAL: {self._fmt(total)}")
        
        if input("\nConfirm? (yes/no): ").strip().lower() == "yes":
            for item in self.cart.items.values():
                self.database.update_appliance_status(item["appliance"]["id"], "Sold")
            self.auth.add_purchase(user['username'])
            self.cart.clear()
            print(f"\n[SUCCESS] Order completed! Total purchases: {user.get('total_purchases', 0)}")
        else:
            print("\nOrder cancelled")
        
        time.sleep(2)
    
    def _check_admin_status(self):
        user = self.auth.get_current_user()
        if not user:
            return
        
        self._clear()
        print("=" * 70 + "\nADMIN STATUS\n" + "=" * 70)
        
        if user["role"] == "admin":
            print("\nYou are already an admin!")
        else:
            print(f"\nRole: {user['role']}")
            print(f"Purchases: {user.get('total_purchases', 0)}/5")
            can_upgrade, msg = self.auth.can_become_admin(user['username'])
            print(f"\n{msg}")
            if can_upgrade:
                print("\nAsk current admin to use option 10!")
        
        input("\nPress ENTER...")
    
    def _add_product(self):
        if not self.auth.is_admin():
            return
        
        self._clear()
        print("=" * 70 + "\n[ADMIN] ADD PRODUCT\n" + "=" * 70)
        
        name = input("\nName: ").strip()
        price = input("Price: ").strip()
        
        if not name or not price.isdigit():
            print("\nInvalid input")
            time.sleep(1)
            return
        
        categories = self.database.get_all_categories()
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        cat_choice = input("\nSelect category: ").strip()
        
        if cat_choice.isdigit():
            idx = int(cat_choice) - 1
            if 0 <= idx < len(categories):
                app_id = self.database.add_appliance(name, int(price), "Available", categories[idx])
                print(f"\nAdded with ID: {app_id}")
                time.sleep(2)
    
    def _make_admin(self):
        if not self.auth.is_admin():
            return
        
        self._clear()
        print("=" * 70 + "\n[ADMIN] MAKE USER ADMIN\n" + "=" * 70)
        
        print("\nUsers:")
        for username, user in self.auth.users.items():
            if username != "admin":
                print(f"- {username} (Role: {user['role']}, Purchases: {user.get('total_purchases', 0)})")
        
        username = input("\nUsername: ").strip()
        password = input("Admin password: ").strip()
        
        success, msg = self.auth.make_admin(username, password)
        print(f"\n{msg}")
        time.sleep(2)
    
    def _exit(self):
        self._clear()
        print("=" * 70 + "\nTHANK YOU FOR VISITING TECH HOUSE!\n" + "=" * 70)
        time.sleep(1)
    
    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
    
    def _fmt(self, price):
        return f"{price:,} UZS"


if __name__ == "__main__":
    app = TechHouseApp()
    app.run()