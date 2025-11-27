from random import randint

class Roll:
    allowed_stats = ["body", "mind", "spirit"]
    def __init__(self, stat, char):
        self.stat = stat

        if stat not in self.allowed_stats:
            raise ValueError(f"'{stat}' is not a recognized stat! Allowed stats are: {', '.join(self.allowed_stats)}")
        
        self.value = max([randint(1,6) for _ in range(getattr(char, stat))])

        print(f"You rolled {self.value}!")

        char.add_stat_boosts(self)