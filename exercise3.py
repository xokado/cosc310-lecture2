"""Exercise 3: Enforce a business rule.

Extend your Cart so invalid operations are rejected by the CART.

ValueError        when qty < 1
OutOfStockError   when the item's "available" field is False
KeyError          when removing an item that is not in the cart

Then demonstrate each one with try/except.
"""

from exercise1 import load_menu


class OutOfStockError(Exception):
    """Raised when a customer tries to order an item that is unavailable."""


class Cart:
    def __init__(self) -> None:
        self.lines: list[dict] = []

    def add_item(self, item: dict, qty: int = 1) -> None:
        # TODO: validate FIRST, then mutate.
        if qty < 1:
            raise ValueError("Quantity must be at least 1")
        if not item["available"]:
            raise OutOfStockError(f"{item['name']} is out of stock")

        for i in self.lines:
            if i["item_id"] == item["id"]:
                i["qty"] += qty
                return

        self.lines.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "qty": qty,
            }
        )

    def remove_item(self, item_id: int) -> None:
        # TODO: raise KeyError if the item is not in the cart
        if not item_id in [i["item_id"] for i in self.lines]:
            raise KeyError(f"Item with id {item_id} not found in cart")
        
        for i in self.lines:
            if i["item_id"] == item_id:
                self.lines.remove(i)
                return

    def total(self) -> float:
        return round(sum(line["price"] * line["qty"] for line in self.lines), 2)

    def __repr__(self) -> str:
        return f"<Cart {len(self.lines)} items, ${self.total():.2f}>"


if __name__ == "__main__":
    menu = load_menu()
    gyoza = menu[1]  # available
    miso = menu[3]  # NOT available

    cart = Cart()

    # TODO: demonstrate each rejection with try/except and a readable message.
    # Example:
    # try:
    #     cart.add_item(gyoza, 0)
    # except ValueError as e:
    #     print(f"Rejected: {e}")

    try:
        cart.add_item(gyoza, 0)
    except ValueError as e:
        print(f"Rejected: {e}")

    try:
        cart.add_item(miso, 1)
    except OutOfStockError as e:
        print(f"Rejected: {e}")
    try:
        cart.remove_item(10)
    except KeyError as e:
        print(f"Rejected: {e}")
