class Item:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class StatBoostItem(Item):

    def __init__(self, *args, stat: str = None, value: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.stat_boost = stat if stat in ["body", "mind", "spirit"] else None
        self.stat_value = value

    def boost_roll(self, roll):
        if roll.stat == self.stat_boost:
            print(f"Din {self.name} giver en bonus på {self.stat_value}!\n")
            roll.value += self.stat_value


class Weapon(StatBoostItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, stat='body')
