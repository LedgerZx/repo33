class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"Product ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock}"

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = []

    def add_to_cart(self, product, quantity):
        if product.stock >= quantity:
            self.cart.append((product, quantity))
            product.stock -= quantity
            print(f"Added {quantity} {product.name}(s) to your cart.")
        else:
            print(f"Sorry, only {product.stock} {product.name}(s) are available.")

    def view_cart(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        print("Your Cart:")
        for product, quantity in self.cart:
            print(f" - {product.name} x{quantity} : ${product.price * quantity:.2f}")
        print(f"Total: ${sum(product.price * quantity for product, quantity in self.cart):.2f}")

    def checkout(self):
        if not self.cart:
            print("Your cart is empty. Nothing to checkout.")
            return
        total = sum(product.price * quantity for product, quantity in self.cart)
        print(f"Checkout successful! Total: ${total:.2f}")
        self.cart = []

class ECommercePlatform:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.load_products()

    def load_products(self):
        # Simulating a product catalog
        products = [
            Product(1, "Laptop", 999.99, 10),
            Product(2, "Smartphone", 499.99, 20),
            Product(3, "Headphones", 99.99, 50),
        ]
        self.products = {product.product_id: product for product in products}

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different one.")
        else:
            self.users[username] = User(username, password)
            print(f"User {username} registered successfully.")

    def login_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            print(f"Welcome, {username}!")
            return user
        else:
            print("Invalid username or password.")
            return None

    def display_products(self):
        print("Product Catalog:")
        for product in self.products.values():
            print(product)

    def main(self):
        while True:
            print("\n1. Register\n2. Login\n3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                self.register_user(username, password)
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.login_user(username, password)
                if user:
                    while True:
                        print("\n1. View Products\n2. View Cart\n3. Checkout\n4. Logout")
                        choice = input("Choose an option: ")
                        if choice == '1':
                            self.display_products()
                            product_id = int(input("Enter product ID to add to cart: "))
                            quantity = int(input("Enter quantity: "))
                            product = self.products.get(product_id)
                            if product:
                                user.add_to_cart(product, quantity)
                            else:
                                print("Invalid product ID.")
                        elif choice == '2':
                            user.view_cart()
                        elif choice == '3':
                            user.checkout()
                        elif choice == '4':
                            print(f"Goodbye, {username}!")
                            break
                        else:
                            print("Invalid choice. Please try again.")
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    platform = ECommercePlatform()
    platform.main()
