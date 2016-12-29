#!/usr/bin/env python3

import itertools
import random
import sys

WELCOME_TEXT = """Welcome {name} to the land of Pavlisha.

Many have entered this land but few have returned.

Your quest is to slay the Bad King, who has stolen the people's Christmas gifts.
"""

ENDING = """
You have defeated the Bad King and saved Christmas.

Merry Christmas {name}!

Love,
Brian, Kevin, Sophie, Pavel and Alex.
"""

DIRECTION_CHOICE = """This place seems very familiar to another but you can't but you can't
put your finger on how...

You are standing in a snow-covered plain. In every direction stretches untracked
miles of trecherous wilderness. Your blood chills at the thought of entering any
of these foreboding landscapes - but enter you must!

To your East lies Mount Doom - a volcano covered in lava and burning embers.
You can smell the sulfer even from here.

To your South lies a nameless forest. You can hear whispers calling you to
enter. They are not kind voices.

To your West lies Swamp Putrid. It's name is well deserved as you can smell the
decaying remains of those who entered before you.

To your feet lies a cave so dark that you can't see into it more than a
sword-length.

Wait...to your North lies a beautiful meadow with a path that winds away from
the terrible danger.

You take a few minutes to rest and then make your choice.
"""

NORTH_TEXT = """You walk north on the idyllic path. You hear bird song, smell the sweet
flowers and see multi-coloured butterflies. The sun is warm and life is good.

Or is it...

"""

NORTH_CONTINUE_TEXT = """Now that the fight is behind you, you continue on the path.

If anything, the flowers smell even sweater than before. Life is great.

Or is it...

"""

EAST_TEXT = """You walk east towards the hellish fires of Mount Doom.

The air reeks of sulfer and you can feel the heat of the lava as you approach.

Occassional pyroclastic blocks fly from the volcano.

"""

EAST_TREE = """At the peak of the volcano you see a single tree. You wonder how it
managed to survive up here.

As your approach, you see that its huge branches have been charred and covered
with a red film. It radiates a sense of potent malevolence.

Just as you are deciding whether to run of not, it charges you and attempts to
crush you with its powerful branches.

"""

EAST_TREE_WIN = """At the base of the tree you spot a golden ingot and a potion.

You put the ingot in your pocket but you aren't sure what to do with the potion.

Oh heck, you are an adventurer aren't you? You sip the potion and suddenly
feel a bit stronger.

"""

SOUTH_TEXT = """You enter the dark forest.

Your sense of foreboding lessens briefly when you see five pigs playing with
other and eating truffles.

Suddenly lightly flashes from the sky and hits the ground near the pigs. The
change before your eyes into horrible Zombie Pigmen.

The moan their hatred of life in general - and you in particular and move
towards you to attack.

Fortunately the forest restricts your movement so that they can only attack you
one at a time.

"""

SOUTH_ALREADY_DONE = """You wonder around the forest for a while but don't
find anything interesting.

You return to the snowy clearing.
"""

SOUTH_END = """You catch your breath amongst the remains of the Zombie Pigmen.

Suddenly, in the corner of your eye, you see a potion laying next to one of
the zombified pigs.

You read the label and it says "Potion of Invisibility". You hide it in your
pack and return to the clearing.
"""

WEST_TEXT = """You walk into the dank swamp hoping not to vomit from the terrible smells.

In the distance you see a huge giant - maybe the smell of decay is coming from
its victims?

As you get closer, you see the smiling, happy face of the giant and realize that
it is a Friendly Giant.

You also see that, behind the giant, there is a Crafting Table and various
magical components! If only you could make use of it for a while...

The giant greats you with a wave and says: "Answer my riddle and the Crafting
Table is yours to use. What gets wetter as it dries?".
"""

WEST_COMPLETED = """You inspect the crafting table and realize that you can use it to
make magical armor and weapons.

You start to work immediately.

After some days, you finish your work and your weapon and armor glow brightly
with their new enchantment!

You walk back to the snowy clearing feeling that there is nothing that you
cannot do with your new magical tools.

Certainly you wouldn't be crushed by flying rocks.
"""

WEST_ALREADY_COMPLETED = """You wander around the swamp until the smell overwealms you.

You return to the snowy clearing.
"""

DOWN_COMMON = """You descend into the dark cave.

There is no light at all but the faint glow of your enchanted armor. You
cautiously proceed, the cold air chilling you to the bone.

Ahead, you see a massive clearing. As it opens up, you see that it is so large
that it contains a huge tower. Guarding the tower is a nearly infinite number
of soliders.
"""

DOWN_VISIBLE = DOWN_COMMON + """You carefully sneak towards the tower, trying to avoid
the attention of the guards.
"""

DOWN_INVISIBLE = DOWN_COMMON + """You drink your potion of invisibility and race towards
the tower. You make it inside just as it wares off!

You climb the circular stairs until the top of the tower. At the top of the
tower you see a medium-sized man sitting in a throne. It is the Bad King!

"Welcome to my tower, {name}." says the Bad King, "I hope that you are
ready to die."

With those words, he picks up his staff and charges towards you.
"""

EAST_AREA = 'east'
SOUTH_AREA = 'south'
WEST_AREA = 'west'
CAVE_AREA = 'cave'

non_clearing_input = input


def my_input(*args, **kwargs):
  import subprocess
  x = non_clearing_input(*args, **kwargs)
  subprocess.call('clear', shell=True)
  return x


input = my_input


class Character:

  def __init__(self, name, dexterity, strength, max_hitpoints):
    self.name = name
    self.dexterity = dexterity
    self.strength = strength
    self.max_hitpoints = max_hitpoints
    self.hitpoints = max_hitpoints
    self.weapon = 'Sword'
    self.armor = 'Chain Mail'
    self.completed_areas = set()
    self.inventory = set()

  def get_damage(self):
    if self.weapon == 'Enchanted Sword':
      return int(random.randint(2, 20) * (self.strength + 50) / 100)
    else:
      return int(random.randint(1, 10) * (self.strength + 50) / 100)

  def __str__(self):
    return """{}

Dexterity: {}
Strength: {}
Hitpoints: {} (of {})
Armor: {}
Weapon: {}
Other Items: {}
""".format(self.name, self.dexterity, self.strength, self.hitpoints,
           self.max_hitpoints, self.armor, self.weapon,
           ', '.join(sorted(self.inventory)) or '<none>')


class CharacterDeadException(BaseException):

  def __init__(self, character):
    pass


def select_character():
  print('What race do you want to be?')
  print()
  print('Elf - Fast but not very strong')
  print('Human - Jack of all trades, master of none')
  print('Orc - Strong but slow')
  print()
  r = ''
  while not r or r[0] not in 'EHO':
    r = input('Enter (E)lf, (H)uman or (O)rc: ').upper().strip()
  if r[0] == 'E':
    dexterity = random.randint(75, 100)
    strength = random.randint(25, 50)
    hitpoints = random.randint(50, 100)
    name = input('What is your name, wise Elf? ')
  elif r[0] == 'H':
    dexterity = random.randint(25, 75)
    strength = random.randint(25, 75)
    hitpoints = random.randint(100, 150)
    name = input('What is your name, bold Human? ')
  else:
    dexterity = random.randint(25, 50)
    strength = random.randint(75, 100)
    hitpoints = random.randint(150, 200)
    name = input('What is your name, strong Orc? ')
  character = Character(name, dexterity, strength, hitpoints)
  print()
  print(character)
  print()
  return character


class Monster:

  def __init__(self, name, hitpoints, dexterity, hitname, missname,
               attack_min_damage, attack_max_damage):
    self.name = name
    self.hitpoints = hitpoints
    self.dexterity = dexterity
    self.hitname = hitname
    self.missname = missname
    self.attack_min_damage = attack_min_damage
    self.attack_max_damage = attack_max_damage


def generate_hit_roll():
  return random.randint(0, 100) + 20


def proceed_after_fight(character, monster):
  while True:
    print()

    hit = generate_hit_roll()
    if hit >= character.dexterity:
      damage = random.randint(monster.attack_min_damage,
                              monster.attack_max_damage)
      character.hitpoints -= damage
      print('The {} {} for {} damage. You have {} hitpoints remaining.'.format(
          monster.name, monster.hitname, damage, character.hitpoints))
    else:
      print('The {} {} - but you dodge away!'.format(monster.name,
                                                     monster.missname))

    if character.hitpoints <= 0:
      raise CharacterDeadException(character)

    c = ''
    while not c or c[0] not in 'AF':
      c = input('What do you want to do? (A)ttack or (F)lee? ').strip().upper()
    if c[0] == 'F':
      print('You cowardly run back to the snowy plains.')
      return False

    hit = generate_hit_roll()
    if hit >= monster.dexterity:
      damage = character.get_damage()
      monster.hitpoints -= damage
      if monster.hitpoints > 0:
        print('You swing your {} at the {} and hit it for {} damage. It has {} '
              'hitpoints remaining.'.format(character.weapon, monster.name,
                                            damage, monster.hitpoints))
      else:
        print("You swing your mighty {} at the {}. It's body will lay as an "
              'example to others who dare to confront you.'.format(
                  character.weapon, monster.name))
        return True
    else:
      print('You swing your mighty {} at the {} but hit nothing but air! Maybe '
            "you aren't cut out for adventuring..."
            .format(character.weapon, monster.name))


def proceed_after_random_fight(character):
  monster = random.choice([
      Monster('Giant Snake',
              random.randint(5, 20),
              random.randint(10, 50), 'slashes you with its giant fangs',
              'strikes at you with its giant fangs', 1, 5),
      Monster('Giant Spider',
              random.randint(1, 10),
              random.randint(1, 10), 'bites you with its poisonous fangs',
              'jumpes to bit you', 5, 20),
      Monster('Skeleton',
              random.randint(1, 10),
              random.randint(10, 20), 'stabs you with its ice sword',
              'swings at you with its ice sword', 2, 10),
      Monster('Zombie',
              random.randint(1, 10),
              random.randint(10, 20), 'cruches you with its decaying arms',
              'tries to grab you with its decaying arms', 2, 10),
      Monster('Orc',
              random.randint(2, 50),
              random.randint(10, 20), 'smashes you with its mace',
              'swings at you with its mace', 20, 50),
  ])
  print('You are attacked by a {}!'.format(monster.name))
  return proceed_after_fight(character, monster)


def go_north(character):
  """Beautiful Meadow."""
  print(NORTH_TEXT)
  while proceed_after_random_fight(character):
    print()
    print(NORTH_CONTINUE_TEXT)


def go_east(character):
  """Mount Doom."""
  print(EAST_TEXT)
  for i in range(0, 150, 25):
    if random.randint(0, i) > character.dexterity:
      print('A block of pyroclastic debris flys towards you. You attempt to '
            'dodge but are\ntoo slow.')
      print()
      if 'Enchanted' in character.armor:
        print('The debris hits your {} and bounces off harmlessly.'.format(
            character.armor))
        print()
        break
      else:
        print(
            'It crushes you into a smoldering pile of bones and burned flesh.')
        print()
        raise CharacterDeadException(character)
    else:
      print('A block of pyroclastic debris flys towards you but you manage to '
            'dodge out\nof the way.')
      c = ''
      while not c or c[0] not in 'CF':
        c = input('Do you go (C)ontinue of (F)lee? ').upper().strip()
      if c[0] == 'F':
        print('You cowardly run back to the snowy plains.')
        return

  if EAST_AREA in character.completed_areas:
    print(
        'At the peak of the volcano, you see the evil tree that you previously'
        ' defeated. You walk back to the snowy clearing.')
    print()
    return

  print()
  print(EAST_TREE)
  evil_tree = Monster('Evil Tree',
                      random.randint(50, 100),
                      random.randint(0, 5),
                      'cruches you with its huge branches',
                      'swings its huge branches towards you', 5, 15)
  if proceed_after_fight(character, evil_tree):
    print(EAST_TREE_WIN)
    character.inventory.add('Golden Ingot')
    strength = character.strength + random.randint(10, 50)
    character.strength += strength
    print('You finish drinking the potion of strengh and gain {} stength. You '
          'now have {} stength.'.format(strength, character.strength))
    print()
    print('You feel like a titan!')
    print()
    print('You walk back to the snowly clearing')
    print()
    character.completed_areas.add(EAST_AREA)


def go_south(character):
  """Forest."""
  if 'Invisibility Potion' in character.inventory:
    print(SOUTH_ALREADY_DONE)
    return

  print(SOUTH_TEXT)
  for i in range(1, 6):
    zombie = Monster('Zombie Pigman #{}'.format(i),
                     random.randint(i * 5, i * 10),
                     random.randint(25, 75), 'stabs you with its wicked sword',
                     'swings its sword at you', i, i * 5)
    if not proceed_after_fight(character, zombie):
      print('You cowardly run back to the snowy plains.')
      print()
      return

  print(SOUTH_END)
  character.inventory.add('Invisibility Potion')


def go_west(character):
  """Swamp."""

  if WEST_AREA in character.completed_areas:
    print(WEST_ALREADY_COMPLETED)
    print()
    return
  print(WEST_TEXT)
  answer = input('What gets wetter as it dries? ').strip()
  if 'towel' not in answer.lower() and 'sponge' not in answer.lower():
    print('"{0}"? "{0}"?! screams the giant. I will smash you into paste!'.
          format(answer))
    print()
    giant = Monster('Friendly Giant', 500, 50, 'smashes you with a giant fist',
                    'tries to step on you', 15, 50)
    if not proceed_after_fight(character, giant):
      print(
          "You cowardly run back to the snowy plains. You hope the giant won't"
          ' remember you in the future.')
      print()
      return
  else:
    print(
        """Yes, towels (and sponges) get wetter as they dry, smiles the giant. He walks away humming."""
    )
    print()
  print(WEST_COMPLETED)
  character.armor = 'Enchanted ' + character.armor
  character.weapon = 'Enchanted ' + character.weapon
  character.completed_areas.add(WEST_AREA)


def go_down(character):
  """Cave."""

  if 'Enchanted' not in character.armor:
    while True:
      character.hitpoints -= 5
      print(
          'The cave is dark and you stubble around until you bump you head on '
          'the ceiling.')
      print('You take {} damage. You have {} hitpoints remaining.'.format(
          5, character.hitpoints))
      if character.hitpoints <= 0:
        raise CharacterDeadException(character)
      c = ''
      while not c or c[0] not in 'CF':
        c = input('Do you want to (C)ontinue or (F)lee? ').upper().strip()
      if c and c[0] == 'F':
        print(
            'You cowardly run back to the snowy plains after a little bump on '
            'the head.')
        print()
        return

  if 'Invisibility Potion' not in character.inventory:
    print(DOWN_VISIBLE)
    for guard_name in itertools.chain(['Guard', 'Guard', 'Strong Guard'],
                                      itertools.repeat('Elite Guard')):
      print(
          'You are spotted by a {} who immediately rushes to defend his king!'.
          format(guard_name))
      if guard_name == 'Guard':
        guard = Monster(guard_name,
                        random.randint(1, 10),
                        random.randint(25, 50), 'stabs you with his spear',
                        'stabs at you with his spear', 1, 10)
      elif guard_name == 'Strong Guard':
        guard = Monster(guard_name,
                        random.randint(10, 20),
                        random.randint(25, 50), 'hits you with his battle axe',
                        'swings his battle axe at you', 2, 20)
      else:
        guard = Monster(guard_name,
                        random.randint(40, 80),
                        random.randint(50, 100),
                        'smashes you with his war hammer',
                        'swings his war hammer at you', 5, 50)
      if not proceed_after_fight(character, guard):
        print('You cowardly run back to the snowy plains. What kind of '
              "adventurer can't get past a few guards?")
        print()
        return

  character.inventory.remove('Invisibility Potion')
  print(DOWN_INVISIBLE.format(name=character.name))
  evil_king = Monster('Bad King', 100, 50, 'hits you with his enchanted staff',
                      'swings at you with his enchanted staff', 5, 10)
  if not proceed_after_fight(character, evil_king):
    print(
        'You cowardly run back to the snowy plains. Did the little king scare '
        'you off?')
    print()
    return
  print(ENDING.format(name=character.name))
  sys.exit(0)


def select_path(character):
  while True:
    print(DIRECTION_CHOICE)
    character.hitpoints = character.max_hitpoints
    c = ''
    while not c or c[0] not in 'NESWDP':
      c = input('Do you go (N)orth (E)ast (S)outh (W)est or (D)own '
                '(P)rint Character? ').upper().strip()
    if c[0] == 'N':
      go_north(character)
    elif c[0] == 'E':
      go_east(character)
    elif c[0] == 'S':
      go_south(character)
    elif c[0] == 'W':
      go_west(character)
    elif c[0] == 'D':
      go_down(character)
    elif c[0] == 'P':
      print(character)
      print()


def main():
  try:
    character = select_character()
    print(WELCOME_TEXT.format(name=character.name))
    select_path(character)
  except CharacterDeadException:
    print("You died. Try again and maybe you'll get lucky.")


if __name__ == '__main__':
  main()
