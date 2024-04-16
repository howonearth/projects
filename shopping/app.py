from cs50 import SQL
import sys

db = SQL("sqlite:///shopping.db")


def main():
    START_TEXT = "\nWhat would you like to do? \n1 to add a shopping list(new shop) \n2 to add products to a shopping list \n3 show an existing shopping list \n4 delete shopping list or product(s) from a shopping list \n5 exit \n"
    print(START_TEXT)
    q = "Your choice: "
    response = validate_response(input(q))

    match response:
        case 1:
            shop = input("What shop do you want to add? ")
            print(add_shop(shop))
            main()
        case 2:
            shop_id = get_shop()
            print(add_shopping_list(shop_id))
            main()
        case 3:
            shop_id = get_shop()
            print("\n".join(get_shopping_list(shop_id)), "\n")
            main()
        case 4:
            answer = get_answer()
            if answer == 1:
                shop_id = get_shop()
                print(delete_shopping_list(shop_id))
                main()
            else:
                shop_id = get_shop()
                print(delete_product(shop_id))
                main()
        case 5:
            sys.exit("Bye! Happy shopping! \n")

def validate_response(response):
    try:
        response = int(response)
        if 0 < response < 6:
            return response
    except ValueError:
        raise ValueError("Not an integer!")

    print("INVALID CHOICE. Expected a number from 1 to 5 \n")
    main()


def add_shop(shop: str) -> str:
    shop = shop.strip().upper()
    try:
        db.execute("INSERT INTO shops(shop) VALUES (?)", shop)
        return f"\n{shop} added!\n"
    except Exception:
        return "\nSomething went wrong\n"


def get_shop() -> int:
    shops = db.execute("SELECT * FROM shops")
    for i, shop in enumerate(shops):
        print(i + 1, "-", shop["shop"])

    while True:
        try:
            the_shop = int(input("\nChoose the shop: ")) - 1
            if the_shop < len(shops) and the_shop >= 0:
                break
            else:
                print("\nInvalid choice: out of range.")
        except ValueError:
            print("\nInvalid choice of the shop. \nPlease, choose a number:")

    name = shops[the_shop]["shop"]
    shop_id = db.execute("SELECT id FROM shops WHERE shop = ?", name)
    shop_id = shop_id[0]["id"]
    print(f"\nSHOP: {name}")
    return shop_id


def add_shopping_list(shop_id):
    print("\nPress Enter to add a product, press Ctrl-D to stop\n")
    while True:
        try:
            product = input("- ").strip().lower()
            db.execute("INSERT INTO products(product, shop_id) VALUES (?, ?)", product, shop_id)
        except EOFError:
            break
    return "\nShopping list updated!\n"


def get_shopping_list(shop_id) -> list:
    sh_list = db.execute("SELECT * FROM products WHERE shop_id = ?", shop_id)
    the_list = list()
    for product in sh_list:
        the_list.append(f"- {product['product']}")
    return the_list

def get_answer():
    while True:
        try:
            answer = int(input("\n1 to delete a shopping list \n2 to delete a product from a shopping list\n\nYour choice: "))
            if answer == 1 or answer == 2:
                return answer
            else:
                print("\nInvalid choice. Choose 1 or 2\n")
        except ValueError:
            print("\nInvalid choice. Choose 1 or 2\n")

def delete_shopping_list(shop_id):
    shop = db.execute("SELECT shop FROM shops WHERE id = ?", shop_id)[0]["shop"]
    confirm = input(f"Are you sure you want to delete the shopping list for {shop}? [yes/no]")

    if confirm.strip().lower() != "yes":
        return "\nAction aborted\n"

    db.execute("DELETE FROM products WHERE shop_id = ?", shop_id)
    db.execute("DELETE FROM shops WHERE id = ?", shop_id)

    return f"\nShopping list for {shop} deleted!\n"


def delete_product(shop_id):
    shop = db.execute("SELECT shop FROM shops WHERE id = ?", shop_id)[0]["shop"]
    shop_list = get_shopping_list(shop_id)
    print("\n".join(shop_list))
    print("\nUsage: Type the name of the product you want to delete, press Enter after each product you want to delete. Press Ctrl-D when you're done.\n")
    products = list()
    while True:
        try:
            product = input("- ").strip().lower()
            products.append(product)
        except EOFError:
            break


    del_products = list()
    not_found = list()

    for product in products:
        if f"- {product}" in shop_list:
            db.execute("DELETE FROM products WHERE product = ?", product)
            del_products.append(product)
        else:
            not_found.append(product)

    return f"Products deleted from {shop} shopping list: {', '.join(del_products)}. Products not found in the list: {', '.join(not_found) if not_found else 'None'}"



if __name__ == "__main__":
    main()
