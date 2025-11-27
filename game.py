from paths import ChoicePath, LinearPath, LootPath, LinearChallengePath
from items import Item, Weapon
from character import Character

wake_up = LinearPath(
    "",
    "You wake up in a bed. You get out of the bed and look around."
)

small_room = ChoicePath(
    "Enter the small room.",
    "You are in a small room. Inside, you see a window, a wardrobe, a bed, and a door."
)
wake_up.set_next(small_room)

# Window path
look_window = ChoicePath(
    "Look out of the window.",
    "You are on the third floor of a castle. Directly beneath the window is a wide moat, and on the other side stretches a green forest as far as the eye can see."
)

jump_out_window = LinearChallengePath(
    "Jump out of the window.",
    "You gracefully drop from the window, and land in the moat, safe and sound!",
    failed="You jump out of the window, but stumble as you set off, landing on your stomach with a splash.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=2,
    stat="body",
)

swim_in_moat = ChoicePath(
    "Swim in the moat.",
    "You tread water in the moat."
)

jump_out_window.set_next(swim_in_moat)

climb_up_wall = LinearChallengePath(
    "Climb up the wall to the window.",
    "You nimbly climb up the wall to the window.",
    failed="You try to climb up the wall, but fall back down.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=4,
    stat="body"
)

climb_up_wall.set_next(small_room)
climb_up_wall.set_failed_next(swim_in_moat)

exit_moat = LinearPath(
    "Exit the moat.",
    "You swim out of the moat, and onto dry land."
)

swim_in_moat.add_choices(climb_up_wall, exit_moat)

# Castle path
front_castle = ChoicePath(
    "Go to the front of the castle.",
    "You stand in front of the castle. Between you and it is a wide moat. The drawbridge is down. Behind you, a green forest stretches for miles and miles."
)
exit_moat.set_next(front_castle)

walk_drawbridge = LinearPath(
    "Walk over the drawbridge.",
    "You cross the drawbridge, and is stopped by an armoured guard. \"Halt!\", the guard says!"
)
sneak_drawbridge = LinearChallengePath(
    "Sneak across the drawbridge.",
    "You deftly sneak across the drawbridge, and past the guard yawning on the other side.",
    failed="As you attempt to sneak across the drawbridge, you step on a creaking board. A nearby armoured guard startles, and approaches you. \"Halt!\", the guard says.",
    challenge=3,
    stat="mind"
)
walk_forest = ChoicePath(
    "Walk into the forest.",
    "You walk into the forest. The trees close in around you, and soon, you can no longer see the sky."
)
front_castle.add_choices(walk_drawbridge, sneak_drawbridge, walk_forest)

# Courtyard path
courtyard = ChoicePath(
    "Walk into the courtyard.",
    "You enter the courtyard inside the castle. The main gate by the drawbridge is guarded by a sleepy, armoured guard. The main entrance to the castle is guarded by two armoured guards. A small door to the side is left ajar."
)
sneak_drawbridge.set_next(courtyard)

drawbridge_guard_in = ChoicePath(
    "Approach the guard at the drawbridge.",
    "You have approached the guard at the drawbridge."
)
sneak_drawbridge.set_failed_next(drawbridge_guard_in)
walk_drawbridge.set_next(drawbridge_guard_in)

drawbridge_guard_in.add_choices(
    LinearChallengePath(
        "Attack the guard.",
        "Your attacks is successful, and the guard retreats.",
        failed="The guard knocks you over the head!",
        failed_consequence=lambda c: c.take_damage(1),
        failed_path=drawbridge_guard_in,
        next_path=courtyard,
        challenge=6,
        stat="body"
    ),
    LinearChallengePath(
        "Pretend to be the castle cook.",
        "\"I am the castle cook,\" you tell the guard. The guard nods and steps aside.",
        failed="\"I am the uh ... Cook?\" you tell the guard. \"Nice try,\" the guard tells you, and shoves you back.",
        failed_consequence=lambda c: c.take_damage(1),
        failed_path=drawbridge_guard_in,
        next_path=courtyard,
        challenge=4,
        stat="mind"
    ),
    LinearChallengePath(
        "Complement the guard's crochet pillow.",
        "\"Hey, that's a nice crochet pillow you got there!\" you say to the guard. \"Thanks, I made it myself!\" the guard says. \"Go on in, friend,\" the guard says, and steps aside.",
        failed="\"Hey, that's a nice ...\" you start to say. The guard shoves you back. \"Get out of here, scum!\" the guard says, rudely.",
        failed_consequence=lambda c: c.take_damage(1),
        failed_path=drawbridge_guard_in,
        next_path=courtyard,
        challenge=3,
        stat="spirit"
    )
)

drawbridge_guard_out = LinearPath(
    "Walk out of the main gate, across the drawbridge.",
    "You walk out of the main gate. As you pass, the guard lazily looks up at you, and nods. You nod back, and cross the drawbridge.",
    next_path=front_castle
)

front_door_guards_in = ChoicePath(
    "Approach the guards at the front door.",
    "You walk up the stairs to the front door. The two guards cross their polearms. \"Halt!\" says one of the guards."
)

side_door_in = LinearChallengePath(
    "Sneak in through the side door.",
    "You deftly and silently open the side door to the castle and walk inside.",
    failed="As you walk towards the side door, the door is pushed open, and a huge man in an appron exits. \"You're late for work,\" he says brusquely and shoves you inside.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=2,
    stat="spirit"
)

courtyard.add_choices(drawbridge_guard_out, front_door_guards_in, side_door_in)

# Small room path
small_sword = Weapon("small sword", value=1)
look_wardrobe = LootPath(
    "Look inside the wardrobe.",
    "Inside the wardrobe is a small sword. Nice!",
    looted_consequence="The wardrobe is empty.",
    loot=small_sword
)

crumpled_note = Item("crumpled note")
look_bed = LootPath(
    "Investigate the bed.",
    "You search the bed. Beneath the sheets, you find a small, crumpled note.",
    looted_consequence="You search the bed, but do not find anything.",
    loot=crumpled_note
)
open_door1 = ChoicePath(
    "Open the door.",
    "You open the door and step outside, letting it shut after you. You are in a long corridor with numerous doors on either side. On the walls are lit torches, and the floor is covered in a thick, red carpet."
)
small_room.add_choices(look_window, look_wardrobe, look_bed, open_door1)
look_window.add_choices(jump_out_window, look_wardrobe, look_bed, open_door1)

# Corridor path
corridor1_left = ChoicePath(
    "Go left.",
    "You go left past numerous doors and torches. As you turn a corner, you hear faint crying coming from a door open ajar to your left."
)
corridor1_right = ChoicePath(
    "Go right.",
    "You go right past numerous doors and torches. As you turn a corner, you see two armored men approaching you. \"Halt!\", one of them says firmly."
)
open_door1.add_choices(corridor1_left, corridor1_right, small_room)

# Left corridor path
walk_in_crying_room = LinearPath(
    "Open the door and walk inside.",
    "You carefully open the door, and enter the room."
)
continue_left1 = ChoicePath(
    "Ignore it, and continue along the corridor.",
    "You ignore the crying, and continue along the corridor. Finally, you make it to a large oak door. Sunlight shines in underneath the door. To your right, a small door is left ajar, and the faint smell of fire and fresh bread meets you from inside."
)
corridor1_left.add_choices(walk_in_crying_room, continue_left1)

# Character creation
char = Character(input("What is your name?: "))

# Initialization
wake_up.choose(char)