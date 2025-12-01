import sys

from time import sleep
from character import Character
from items import Item
from roll import Roll

GAME_SPEED = 50


def wait_print(message):
    print(message)
    sleep(len(message)/GAME_SPEED)


class SimplePath:

    def __init__(self, action: str, consequence: str, back=None, after=None, requirement=None):
        self.action = action
        self.consequence = consequence
        self.back = back
        self.after = after
        self.requirement = requirement

    def choose(self, char, *args, silent: bool = False):
        self.clean_up(char)
        if not silent:
            wait_print(f"\n{self.consequence}")

    def clean_up(self, char):
        if self.after:
            self.after(char)

    def __str__(self):
        return self.action

    def __repr__(self):
        return f'<{self.__class__.__name__}: "{self.action[:20]} ..., {self.consequence[:20]} ...">'

    def can_choose(self, char):
        return self.requirement(char)


class LinearPath(SimplePath):

    def __init__(self, *args, next_path: SimplePath = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_path = None

        if next_path:
            self.set_next(next_path)

    def set_next(self, path: SimplePath):
        self.next_path = path
        path.back = self

    def choose(self, char, *args, **kwargs):
        super().choose(char, *args, **kwargs)

        if self.next_path:
            self.next_path.back = self
            self.next_path.choose(char, *args)

        else:
            self.back.choose(char, *args, silent=True)


class EndPath(SimplePath):

    def __init__(self, *args, credits: list[str] = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.credits = credits

    def choose(self, char: Character, *args, **kwargs):
        super().choose(char, *args, **kwargs)

        print("\nTak fordi du spillede! Denne historie er lavet af:")
        for cred in self.credits:
            wait_print(f"  {cred}")

        char.show_stats()

        char.show_inventory()

        sys.exit(1)


class LinearChallengePath(LinearPath):

    def __init__(self, *args, failed: str = None, failed_consequence=None,
                 succeeded_consequence=None, failed_path: SimplePath = None, challenge: int = 4,
                 success_consequence=None,
                 stat: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = failed
        self.failed_consequence = failed_consequence
        self.succeeded_consequence = succeeded_consequence
        self.success_consequence = success_consequence
        self.failed_path = None
        self.challenge = challenge
        self.stat = stat if stat in ["body", "mind", "spirit"] else None
        self.succeeded = False

        if failed_path:
            self.set_failed_next(failed_path)

    def set_failed_next(self, path: SimplePath):
        self.failed_path = path
        path.back = self

    def increase_challenge(self, value: int = 1):
        self.challenge += value

    def choose(self, char: Character, *args, **kwargs):
        if self.succeeded:
            if self.succeeded_consequence:
                self.consequence = self.succeeded_consequence
            super().choose(char, *args)

        else:
            roll = Roll(self.stat, char)

            success = roll.value >= self.challenge

            if success:
                self.succeeded = True
                if self.success_consequence:
                    self.success_consequence(char)

                super().choose(char, *args)

            else:
                wait_print(self.failed)

                if self.failed_consequence:
                    self.failed_consequence(char)

                if self.failed_path:
                    self.failed_path.back = self
                    self.failed_path.choose(char, *args)
                elif self.next_path:
                    self.next_path.back = self
                    self.next_path.choose(char, *args)
                else:
                    self.back.choose(char, *args, silent=True)


class LootPath(SimplePath):

    def __init__(self, *args, loot: Item = None, looted_consequence: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loot = loot
        self.looted = False
        self.looted_consequence = looted_consequence

    def choose(self, char: Character, **kwargs):
        super().choose(char, **kwargs)

        if self.loot and not self.looted:
            take_item = input(
                f"\nVil du tage {self.loot}? (J/n): ").lower() != "n"

            if take_item:
                char.add_item(self.loot)
                self.looted = True
                self.consequence = self.looted_consequence
                print(f"\nDu tog {self.loot.name}!")

        self.back.choose(char, silent=True)


class LootLinearPath(LinearPath):

    def __init__(self, *args, loot: Item = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loot = loot
        self.looted = False

    def choose(self, char: Character, **kwargs):

        if self.loot and not self.looted:
            take_item = input(
                f"Vil du tage {self.loot}? (J/n): ").lower() != "n"

            if take_item:
                char.add_item(self.loot)
                self.looted = True
                print(f"Du tog {self.loot.name}!")

        print("Nuværende genstande:", char.inventory)

        super().choose(char, **kwargs)


class ChoicePath(SimplePath):

    def __init__(self, *args):
        super().__init__(*args)
        self.choices = []

    def add_choice(self, path: SimplePath):
        self.choices.append(path)
        path.back = self

    def add_choices(self, *paths: SimplePath):
        for path in paths:
            self.add_choice(path)

    def rem_choice(self, path: SimplePath):
        self.choices.remove(path)
        path.back = None

    def rem_choices(self, *paths: SimplePath):
        for path in paths:
            self.rem_choice(path)

    def set_choices(self, *paths: SimplePath):
        self.choices = []
        self.add_choices(*paths)

    def choose(self, char: Character, *args, **kwargs):
        super().choose(char, *args, **kwargs)

        if self.choices:
            print("\nHvad vil du gøre?")
            pos_choices = [
                choice for choice in self.choices if choice.can_choose(char)]
            for i, choice in enumerate(pos_choices):
                print(f"({i+1}): {choice.action}")

            choice = None
            while not choice:
                try_choice = input("Vælg et tal: ")

                if try_choice in ["i", "g"]:
                    char.show_inventory()
                elif try_choice in ["c", "s", "k"]:
                    char.show_stats()
                else:

                    try:
                        int_choice = int(try_choice)
                    except ValueError:
                        print("Indsæt kun et tal!")
                        continue

                    if 1 > int_choice > len(self.choices):
                        print(
                            f"Indsæt et tal mellem 1 og {len(self.choices)}, tak.")
                    else:
                        choice = self.choices[int_choice-1]

            choice.back = self
            choice.choose(char, *args)

        else:
            self.back.choose(char, silent=True)


class HasItemLinearPath(LinearPath):

    def __init__(self, *args, required_item: Item = None, failed: str = "",
                 failed_path: SimplePath = None, success_consequence=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_item = required_item
        self.failed = failed
        self.failed_path = failed_path
        self.success_consequence = success_consequence

    def set_failed_next(self, path: SimplePath):
        self.failed_path = path
        path.back = self

    def choose(self, char: Character, **kwargs):
        if char.has_item(self.required_item):
            if self.success_consequence:
                self.success_consequence(char)
            super().choose(char, **kwargs)
        else:
            wait_print(self.failed)

            if self.failed_path:
                self.failed_path.back = self
                self.failed_path.choose(char, **kwargs)
            elif self.next_path:
                self.next_path.back = self
                self.next_path.choose(char, **kwargs)
            else:
                self.back.choose(char, silent=True)
