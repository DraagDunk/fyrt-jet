from time import sleep
from character import Character
from items import Item
from roll import Roll

GAME_SPEED = 100

def wait_on(message):
    sleep(len(message)/GAME_SPEED)

class SimplePath:

    def __init__(self, action:str, consequence:str, back = None):
        self.action = action
        self.consequence = consequence
        self.back = back

    def choose(self, *args, silent:bool=False):
        if not silent:
            print("\n"+self.consequence)
            wait_on(self.consequence)

    def __str__(self):
        return self.action
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: "{self.action[:20]} ..., {self.consequence[:20]} ...">'


class LinearPath(SimplePath):

    def __init__(self, *args, next_path:SimplePath=None):
        super().__init__(*args)
        self.next_path = None

        if next_path:
            self.set_next(next_path)

    def set_next(self, path: SimplePath):
        self.next_path = path
        path.back = self

    def choose(self, *args, **kwargs):
        super().choose(*args, **kwargs)
        
        if self.next_path:
            self.next_path.choose(*args)

        else:
            self.back.choose(*args, silent=True)


class LinearChallengePath(LinearPath):

    def __init__(self, *args, failed:str=None, failed_consequence=None, succeeded_consequence=None, failed_path:SimplePath=None, challenge:int=4, stat:str=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = failed
        self.failed_consequence = failed_consequence
        self.succeeded_consequence = succeeded_consequence
        self.failed_path = None
        self.challenge = challenge
        self.stat = stat if stat in ["body", "mind", "spirit"] else None
        self.succeeded = False

        if failed_path:
            self.set_failed_next(failed_path)

    def set_failed_next(self, path: SimplePath):
        self.failed_path = path
        path.back = self

    def choose(self, char: Character, *args, **kwargs):
        if self.succeeded:
            super().choose(char, *args)

        else:
            roll = Roll(self.stat, char)

            success = roll.value >= self.challenge

            if success:
                super().choose(char, *args)
                self.succeeded = True
                self.consequence = self.succeeded_consequence

            else:
                print(self.failed)
                wait_on(self.failed)
                
                if self.failed_consequence:
                    self.failed_consequence(char)

                if self.failed_path:    
                    self.failed_path.choose(char, *args)
                elif self.next_path:
                    self.next_path.choose(char, *args)
                else:
                    self.back.choose(char, *args, silent=True)


class LootPath(SimplePath):

    def __init__(self, *args, loot:Item=None, looted_consequence:str=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loot = loot
        self.looted = False
        self.looted_consequence = looted_consequence

    def choose(self, char: Character, **kwargs):
        super().choose(**kwargs)
        
        if self.loot and not self.looted:
            take_item = input("Do you want to take it? (Y/n): ").lower() != "n"

            if take_item:
                char.add_item(self.loot)
                self.looted = True
                self.consequence = self.looted_consequence
                print(f"You took the {self.loot.name}!")

        print("Current inventory:", char.inventory)

        self.back.choose(char, silent=True)


class ChoicePath(SimplePath):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.choices = []

    def add_choice(self, path:SimplePath):
        self.choices.append(path)
        path.back = self

    def add_choices(self, *paths:SimplePath):
        for path in paths:
            self.add_choice(path)

    def choose(self, char, *args, **kwargs):
        super().choose(char, *args, **kwargs)

        if self.choices:
            print("\nWhat do you want to do?")
            for i, choice in enumerate(self.choices):
                print(f"({i+1}): {choice.action}")

            choice = None
            while not choice:
                try_choice = input("Chooce a number: ")

                try:
                    int_choice = int(try_choice)
                except ValueError:
                    print("Input just a number please!")
                    continue

                if 1 > int_choice > len(self.choices):
                    print(f"Input a number between 1 and {len(self.choices)} please.")
                else:
                    choice = self.choices[int_choice-1]

            choice.choose(char, *args)

        else:
            self.back.choose(char,silent=True)

                