from membership import Membership


class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_item(self, appliance, quantity=1):
        """Add an appliance to the cart with a chosen quantity"""
        if not appliance or "id" not in appliance:
            return False

        try:
            quantity = int(quantity)
        except ValueError:
            return False

        if quantity <= 0:
            return False

        appliance_id = appliance["id"]

        if appliance_id in self.items:
            self.items[appliance_id]["quantity"] += quantity
        else:
            self.items[appliance_id] = {
                "appliance": appliance.copy(),
                "quantity": quantity
            }
        return True

    def remove_item(self, appliance_id):
        """Remove the whole product from the cart"""
        if appliance_id in self.items:
            del self.items[appliance_id]
            return True
        return False

    def remove_quantity(self, appliance_id, quantity=1):
        """Decrease quantity. If quantity becomes 0 or less, remove the item."""
        if appliance_id not in self.items:
            return False

        try:
            quantity = int(quantity)
        except ValueError:
            return False

        if quantity <= 0:
            return False

        self.items[appliance_id]["quantity"] -= quantity

        if self.items[appliance_id]["quantity"] <= 0:
            del self.items[appliance_id]

        return True

    def set_quantity(self, appliance_id, quantity):
        """Set exact quantity. If quantity <= 0, removes the item."""
        if appliance_id not in self.items:
            return False

        try:
            quantity = int(quantity)
        except ValueError:
            return False

        if quantity <= 0:
            del self.items[appliance_id]
            return True

        self.items[appliance_id]["quantity"] = quantity
        return True

    # (optional) keep old name for compatibility
    def update_quantity(self, appliance_id, quantity):
        return self.set_quantity(appliance_id, quantity)

    def get_total(self, membership_package=None):
        total = 0
        for item in self.items.values():
            price = item["appliance"]["price"]
            quantity = item["quantity"]

            if membership_package:
                price = Membership.calculate_discount(price, membership_package)
                price = round(price)

            total += price * quantity
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
        print("\n" + "=" * 70)
        print("SHOPPING CART")
        print("=" * 70)

        if self.is_empty():
            print("\nYour cart is empty")
            return

        print(f"\n{'Product':<35} {'Qty':>5} {'Price':>12} {'Subtotal':>12}")
        print("-" * 70)

        original_total = 0
        discounted_total = 0

        for item in self.items.values():
            appliance = item["appliance"]
            quantity = item["quantity"]
            original_price = appliance["price"]

            # discounted price (if membership exists)
            final_price = original_price
            if membership_package:
                final_price = Membership.calculate_discount(original_price, membership_package)

            original_subtotal = original_price * quantity
            final_subtotal = final_price * quantity

            original_total += original_subtotal
            discounted_total += final_subtotal

            # Truncate long names
            name = appliance["name"]
            if len(name) > 30:
                name = name[:27] + "..."

            print(f"{name:<35} {quantity:>5} "
                f"{self._format_price(final_price):>12} "
                f"{self._format_price(final_subtotal):>12}")

            # If discounted, show original + savings clearly under the item
            if final_price < original_price:
                save_per_item = original_price - final_price
                save_total_item = original_subtotal - final_subtotal
                print(f"{'':<2}Original: {self._format_price(original_price)}"
                    f" | Save: {self._format_price(save_per_item)} each"
                    f" ({self._format_price(save_total_item)} total)")

        if membership_package:
            package_info = Membership.get_package_info(membership_package)
            if package_info:
                print("-" * 70)
                print(f"Membership: {membership_package} ({package_info['discount']}% discount)")

        print("-" * 70)
        print(f"{'TOTAL (after discount)':<35} {self.get_item_count():>5} "
            f"{' '*12} {self._format_price(discounted_total):>12}")

        # Show savings summary (only if a discount applied)
        savings = original_total - discounted_total
        if savings > 0:
            print(f"{'TOTAL (before discount)':<35} {'':>5} "
                f"{' '*12} {self._format_price(original_total):>12}")
            print(f"{'YOU SAVE':<35} {'':>5} "
                f"{' '*12} {self._format_price(savings):>12}")


    def _format_price(self, price):
        return f"{int(price):,} UZS"