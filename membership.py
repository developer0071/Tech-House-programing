from datetime import datetime, timedelta


class Membership:
    
    PACKAGES = {
        "Bronze": {
            "discount": 5,
            "free_delivery": False,
            "description": "Entry level membership with 5% discount"
        },
        "Silver": {
            "discount": 10,
            "free_delivery": False,
            "description": "Mid-tier membership with 10% discount"
        },
        "Gold": {
            "discount": 15,
            "free_delivery": True,
            "description": "Premium membership with 15% discount and free delivery"
        }
    }
    
    @staticmethod
    def get_package_info(package_name):
        if not package_name:
            return None
        return Membership.PACKAGES.get(package_name, None)
    
    @staticmethod
    def calculate_discount(price, package_name):
        if not package_name:
            return price
            
        package = Membership.get_package_info(package_name)
        if package:
            discount = package["discount"]
            discounted_price = price * (1 - discount / 100)
            return round(discounted_price)
        return price
    
    @staticmethod
    def has_free_delivery(package_name):
        if not package_name:
            return False
        package = Membership.get_package_info(package_name)
        return package and package.get("free_delivery", False)
    
    @staticmethod
    def is_valid_package(package_name):
        return package_name in Membership.PACKAGES
    
    @staticmethod
    def get_all_packages():
        return list(Membership.PACKAGES.keys())
    
    @staticmethod
    def display_packages():
        print("\n" + "=" * 70)
        print("MEMBERSHIP PACKAGES")
        print("=" * 70)
        
        for name, info in Membership.PACKAGES.items():
            print(f"\n{name.upper()}")
            print(f"  Discount: {info['discount']}%")
            print(f"  Free Delivery: {'Yes' if info['free_delivery'] else 'No'}")
            print(f"  {info.get('description', '')}")