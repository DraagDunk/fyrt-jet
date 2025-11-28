import sys

from items import Item
from roll import Roll


class Character:
    def __init__(self, name):
        self.name = name
        if name == "Hans Christian":
            self.body = 100
            self.mind = 100
            self.spirit = 100
            self.health = 101
            self.max_health = 101
        else:
            self.body = 1
            self.mind = 1
            self.spirit = 1
            self.health = 3
            self.max_health = 3
        self.inventory = []

    def add_item(self, item: Item):
        self.inventory.append(item)

    def remove_item(self, item: Item):
        self.inventory.remove(item)

    def show_inventory(self):
        print("\n| Genstande:")
        for item in self.inventory:
            print(f"| * {str(item).capitalize()}")
        print("\n")

    def show_stats(self):
        print(f"\n| Navn: {self.name}")
        print(f"| Helbred: {self.health}/{self.max_health}")
        print(f"| Krop: {self.body}")
        print(f"| Sind: {self.mind}")
        print(f"| Ånd:  {self.spirit}")
        print("\n")

    def check_death(self):
        if self.health <= 0:
            print("\nDu døde, beklager!")
            sys.exit(1)

    def take_damage(self, value):
        self.health -= value
        print(f"\nDu tager {value} skade!")
        self.check_death()

    def add_stat_boosts(self, roll: Roll):
        for item in self.inventory:
            if hasattr(item, 'stat_boost'):
                item.boost_roll(roll)

    def has_item(self, item: Item):
        for it in self.inventory:
            if it == item:
                return True
        else:
            return False
