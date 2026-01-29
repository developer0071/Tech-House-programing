from membership import Membership


class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_item(self, appliance, quantity=1):
        if not appliance or "id" not in appliance or not self._is_valid_quantity(quantity):
            return False

        appliance_id = appliance["id"]

        if appliance_id in self.items:
            self.items[appliance_id]["quantity"] += int(quantity)
        else:
            self.items[appliance_id] = {"appliance": appliance.copy(), "quantity": int(quantity)}
        return True

    def remove_item(self, appliance_id):
        if appliance_id in self.items:
            del self.items[appliance_id]
            return True
        return False

    def remove_quantity(self, appliance_id, quantity=1):
        if appliance_id not in self.items or not self._is_valid_quantity(quantity):
            return False

        self.items[appliance_id]["quantity"] -= int(quantity)

        if self.items[appliance_id]["quantity"] <= 0:
            del self.items[appliance_id]

        return True

    def set_quantity(self, appliance_id, quantity):
        if appliance_id not in self.items:
            return False

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return False

        if quantity <= 0:
            del self.items[appliance_id]
        else:
            self.items[appliance_id]["quantity"] = quantity
        
        return True

    def update_quantity(self, appliance_id, quantity):
        return self.set_quantity(appliance_id, quantity)

    def get_total(self, membership_package=None):
        total = 0
        for item in self.items.values():
            price = item["appliance"]["price"]
            if membership_package:
                price = round(Membership.calculate_discount(price, membership_package))
            total += price * item["quantity"]
        return round(total)

    def get_item_count(self):
        return sum(item["quantity"] for item in self.items.values())

    def get_unique_item_count(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return len(self.items) == 0

    def get_items(self):
        return self.items.copy()

    def display(self, membership_package=None):
        print("SHOPPING CART")

        if self.is_empty():
            print("\nYour cart is empty")
            return

        print(f"\n{'Product':<35} {'Qty':>5} {'Price':>12} {'Subtotal':>12}")

        original_total = discounted_total = 0

        for item in self.items.values():
            appliance = item["appliance"]
            quantity = item["quantity"]
            original_price = appliance["price"]

            final_price = round(Membership.calculate_discount(original_price, membership_package)) if membership_package else original_price

            original_subtotal = original_price * quantity
            final_subtotal = final_price * quantity

            original_total += original_subtotal
            discounted_total += final_subtotal

            name = appliance["name"][:27] + "..." if len(appliance["name"]) > 30 else appliance["name"]

            print(f"{name:<35} {quantity:>5} {self._format_price(final_price):>12} {self._format_price(final_subtotal):>12}")

            if final_price < original_price:
                print(f"{'':<2}Original: {self._format_price(original_price)}"
                      f" | Save: {self._format_price(original_price - final_price)} each"
                      f" ({self._format_price(original_subtotal - final_subtotal)} total)")

        if membership_package:
            package_info = Membership.get_package_info(membership_package)
            if package_info:
                print("-" * 70)
                print(f"Membership: {membership_package} ({package_info['discount']}% discount)")

        print("-" * 70)
        print(f"{'TOTAL (after discount)':<35} {self.get_item_count():>5} {' '*12} {self._format_price(discounted_total):>12}")

        savings = original_total - discounted_total
        if savings > 0:
            print(f"{'TOTAL (before discount)':<35} {'':>5} {' '*12} {self._format_price(original_total):>12}")
            print(f"{'YOU SAVE':<35} {'':>5} {' '*12} {self._format_price(savings):>12}")

    def _is_valid_quantity(self, quantity):
        try:
            return int(quantity) > 0
        except (ValueError, TypeError):
            return False

    def _format_price(self, price):
        return f"{int(price):,} UZS"