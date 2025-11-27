import sys

from items import Item
from roll import Roll

class Character:
    def __init__(self, name):
        self.name = name
        self.body = 1
        self.mind = 1
        self.spirit = 1
        self.health = 3
        self.inventory = []

    def add_item(self, item:Item):
        self.inventory.append(item)

    def check_death(self):
        if self.health <= 0:
            print("\nYou died, sorry!")
            sys.exit(1)

    def take_damage(self, value):
        self.health -= value
        self.check_death()

    def add_stat_boosts(self, roll:Roll):
        for item in self.inventory:
            if hasattr(item, 'stat_boost'):
                item.boost_roll(roll)