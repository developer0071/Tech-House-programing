from datetime import datetime, timedelta


class Membership:
    
    PACKAGES = {
        "Bronze": {
            "discount": 5,
            "free_delivery": False
        },
        "Silver": {
            "discount": 10,
            "free_delivery": False
        },
        "Gold": {
            "discount": 15,
            "free_delivery": True
        }
    }
    
    @staticmethod
    def get_package_info(package_name):
        return Membership.PACKAGES.get(package_name, None)
    
    @staticmethod
    def calculate_discount(price, package_name):
        package = Membership.get_package_info(package_name)
        if package:
            discount = package["discount"]
            return price * (1 - discount / 100)
        return price
    
    @staticmethod
    def has_free_delivery(package_name):
        package = Membership.get_package_info(package_name)
        return package and package["free_delivery"]
    
    @staticmethod
    def display_packages():
        print("\n" + "=" * 70)
        print("MEMBERSHIP PACKAGES")
        print("=" * 70)
        for name, info in Membership.PACKAGES.items():
            print(f"\n{name.upper()}")
            print(f"  Discount: {info['discount']}%")
            print(f"  Free Delivery: {'Yes' if info['free_delivery'] else 'No'}")