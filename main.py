from collections import defaultdict

class Item:
    def __init__(self, name, price, calories):
        self.name = name
        self.price = price
        self.calories = calories

class Slot:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

class MoneyBox:
    def __init__(self):
        self.funds = defaultdict(int) # Hashmap/Dictionary for denominations

    def add_funds(self, denominations):
        for denom in denominations:
            self.funds[denom] += 1
        print(f"Added funds. Current balance: ${self.get_total()}")

    def get_total(self):
        total = 0
        for denom, count in self.funds.items():
            total += denom * count
        return total


class VendingMachine:
    def __init__(self, items):
        self.money_box = MoneyBox()
        self.slots = [Slot(item, 10) for item in items]
        self.transaction_summary = {item.name: 0 for item in items}

    def show_items(self):
        for i, slot in enumerate(self.slots, 1):
            print(f"Slot {i} - {slot.item.name}, Price: ${slot.item.price}, Calories: {slot.item.calories}, Quantity: {slot.quantity}")

    def change_item_price(self, slot_number, new_price):
        slot = self.slots[slot_number - 1]
        slot.item.price = new_price
        print(f"Price of {slot.item.name} changed to ${new_price}")

    # Method to collect payment
    def collect_payment(self):
        collected_amount = self.money_box.get_total()
        self.money_box = MoneyBox()
        print(f"Collected ${collected_amount} from the machine.")

    def restock(self):
        for slot in self.slots:
            slot.quantity = 10

    def print_transaction_summary(self):
        print("Transaction Summary:")
        for item, quantity in self.transaction_summary.items():
            print(f"{item}: {quantity}")
        print(f"Total funds: ${self.money_box.get_total()}")

    def buy_item(self, slot_number):
        slot = self.slots[slot_number - 1]
        if self.money_box.get_total() < slot.item.price: # Using get_total() method to get the total amount of funds
            print("Insufficient funds.")
        elif slot.quantity == 0:
            print(f"{slot.item.name} is out of stock.")
        else:
            # Assuming the price of the item exactly matches a denomination in the money box
            if self.money_box.funds[slot.item.price] > 0:
                self.money_box.funds[slot.item.price] -= 1
                slot.quantity -= 1
                self.transaction_summary[slot.item.name] += 1
                print(f"Vending {slot.item.name}. Remaining balance: ${self.money_box.get_total()}")
            else:
                print("Sorry, no exact change available.")

    def show_items(self):
        for i, slot in enumerate(self.slots, 1):
            print(f"Slot {i} - {slot.item.name}, Price: ${slot.item.price}, Calories: {slot.item.calories}, Quantity: {slot.quantity}")

    def change_item_price(self, slot_number, new_price):
        slot = self.slots[slot_number - 1]
        slot.item.price = new_price
        print(f"Price of {slot.item.name} changed to ${new_price}")

    # Method to collect payment
    def collect_payment(self):
        collected_amount = self.money_box.funds
        self.money_box.funds = 0
        print(f"Collected ${collected_amount} from the machine.")

    # Method to replenish money for change
    def replenish_money(self, amount):
        self.money_box.funds += amount
        print(f"Replenished money box. Current balance: ${self.money_box.funds}")

    def add_funds(self, amount):
        self.money_box.funds += amount

    def restock(self):
        for slot in self.slots:
            slot.quantity = 10

    def print_transaction_summary(self):
        print("Transaction Summary:")
        for item, quantity in self.transaction_summary.items():
            print(f"{item}: {quantity}")
        print(f"Total funds: ${self.money_box.funds}")

    def buy_item(self, slot_number):
        slot = self.slots[slot_number - 1]
        if self.money_box.funds < slot.item.price:
            print("Insufficient funds.")
        elif slot.quantity == 0:
            print(f"{slot.item.name} is out of stock.")
        else:
            self.money_box.funds -= slot.item.price
            slot.quantity -= 1
            self.transaction_summary[slot.item.name] += 1
            print(f"Vending {slot.item.name}. Remaining balance: ${self.money_box.funds}")

class SpecialVendingMachine(VendingMachine):
    def buy_item(self, slot_numbers):
        for slot_number in slot_numbers:
            slot = self.slots[slot_number - 1]
            if self.money_box.funds < slot.item.price:
                print("Insufficient funds.")
            elif slot.quantity == 0:
                print(f"{slot.item.name} is out of stock.")
            else:
                self.money_box.funds -= slot.item.price
                slot.quantity -= 1
                self.transaction_summary[slot.item.name] += 1
                print(f"Adding {slot.item.name}...")
        print(f"Special item prepared! Remaining balance: ${self.money_box.funds}")

class VendingMachineFactory:
    def __init__(self, items):
        self.vending_machine = None
        self.items = items

    def main_menu(self):
        while True:
            print("\n1. Create regular vending machine\n2. Create special vending machine\n3. Test vending machine\n4. Exit")
            option = int(input("Choose option: "))
            if option == 1:
                self.create_vending_machine(special=False)
            elif option == 2:
                self.create_vending_machine(special=True)
            elif option == 3:
                self.test_vending_machine()
            elif option == 4:
                print("Exiting...")
                break
            else:
                print("Invalid option.")

    def create_vending_machine(self, special=False):
        if special:
            self.vending_machine = SpecialVendingMachine(self.items)
        else:
            self.vending_machine = VendingMachine(self.items)

    def test_vending_machine(self):
        if not self.vending_machine:
            print("No vending machine available.")
            return
        while True:
            print(
                "\n1. Show items\n2. Add funds\n3. Buy item\n4. Restock\n5. Print transaction summary\n6. Back to main menu")
            option = int(input("Choose option: "))
            if option == 1:
                self.vending_machine.show_items()
            elif option == 2:
                denominations = list(map(int, input("Enter denominations (separated by space): ").split()))
                self.vending_machine.money_box.add_funds(denominations)
            elif option == 3:
                if isinstance(self.vending_machine, SpecialVendingMachine):
                    slot_numbers = list(map(int, input("Enter slot numbers (separated by space): ").split()))
                else:
                    slot_number = int(input("Enter slot number: "))
                    slot_numbers = [slot_number]
                self.vending_machine.buy_item(slot_numbers)
            elif option == 4:
                self.vending_machine.restock()
            elif option == 5:
                self.vending_machine.print_transaction_summary()
            elif option == 6:
                slot_number = int(input("Enter slot number: "))
                new_price = float(input("Enter new price: "))
                self.vending_machine.change_item_price(slot_number, new_price)
            elif option == 7:
                self.vending_machine.collect_payment()
            elif option == 8:
                amount = float(input("Enter amount to replenish: "))
                self.vending_machine.replenish_money(amount)
            elif option == 9:
                break
            else:
                print("Invalid option.")

def main():
    items = [Item("Noodles", 2.0, 200), Item("Egg", 1.0, 70), Item("Chashu Pork", 3.0, 250), Item("Fried Tofu", 2.0, 150), Item("Negi", 0.5, 20), Item("Tonkotsu Broth", 1.5, 100), Item("Ukokkei Broth", 2.0, 120), Item("Miso Broth", 1.5, 110)]
    factory = VendingMachineFactory(items)
    factory.main_menu()

if __name__ == "__main__":
    main()
