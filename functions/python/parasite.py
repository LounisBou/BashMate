#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Import the random module
import random
import sys

# Parasite sequences
##
##
##
PARASITES = ['̶̬̯̻̾͊͂', '̵̜͔̭̃̈́͂̑̑̓͌̐̋̂̚̚͘͝͠', '̴̻̜͖̘̹͙̭̙͇̻̈́́̚', '̵̢̦͇̐̃̋̈́͗͂̓̇̈͛̅̏̕͝͝', '̴̞͈͓͐̓̎͋̚͝', '̶̨̡͙͙̞̖͇̩̖͚̙͇̹͔̘̃͛̉', '̶̣̠̙̑͋̿͑̈́̉̀̀̈́͌͛̈̏̀̄', '̶̫̱̥̟̤̺͔̯̱͚͛̾̾̿͘ͅ', '̷̮̺̜̘̯͉͕͕͚̾̿͊̃̚͜͝͠', '̷̛̬͚̳̗͓͓̹̫͙͋̄̀̀͗̓̈́', '̴̠͓̤̣̟͙͓̬̗̊̾̈́̀̈́̈́̀̎̕', '̷̝̖͍̗͍̪̯̼̯̻͋̈', '̸̢̠̜̱͈͍̄̉͑̕͠͝', '̷̠̳̠̳̞̇̔', '̴̖̟͙͎̱̓͐̋̕', '̴̢̨̢̺̩̤͇̟̲̄̌̂̕', '̸̞̦̘̠̼͎͖̬̘͌̎͐̓͒̚͘͝ͅ', '̴̥́̉́̉̅̌̓̍́͑̽̚̚', '̸̼͎̜͎͎͂͒̓͑̈́͒̓̕͘͜͜͝͠', '̸͖̌̕͝͝', '̵̧̲̤̬͛̎͋̏͂̎̉͊́͒̈̽̚̕', '̴̯̟̜͎̆͆̽̊͌̅̏̀̓̇̋̚͠͠', '̵̡̧̧̫̦̥̫͚͉͕̺̐̈́̌͋̔͒̈', '̴͖̘͚̩̮̩̹̮̹̀̈́́͌̾͗̓͠͝', '̵̧̣̝̩̲̮̘̳͇̔̂̀͑́̐́̇͜', '̷̛̛̛͕͉̺̓̀̀̽̅̇̊͋̄̿̈́̀', '̸̡̛͚̰̭̼̹͍̎̄̄͘͘̚', '̶̦͇̬̰̒̌͆̂̐̌̈́͆͋̎̀', '̴͚̗̏̑͛̋̈̀̇̒̓̈́͆̍̽', '̶̨͔̺̱͙̪̳̬̺̭̦̒̾̅̄̕̚͜', '̶̢̧͈͇̝̝̰̖͍̅͠͠', '̴̮́͌', '̴̞̀̽̈́', '̴̧̟̞̞̜̖̬͕͈̳͈͕̯̣̇̎', '̷̢̛̣̣͙̋̚', '̶͍͇̪̿', '̵̭̆̽̒̅̊̋̈́̐́̆͘', '̷̫͙͇͕́̔͊͑̐͘͠', '̸̢̡͎̙̮̻̻̼̬̬̇͆͛̆̈̒͘͠', '̷̥͍͓͍͛͌͆̐̐̀͑̀̆̉͐̕͘͠', '̸͕̟̣̩̽̉͋̈̈́͑̕͝͠', '̵̗̠̑̐', '̶̳̘͓̪̯̀̇̈́͌̿̿̂͘͠ͅ', '̶̡̧̨̤̺̬̣̤͕̺̖͓̬͗͑͒́ͅ', '̴̧̧̩͓͇̜͚́̃̍̆́̄͗͗͛̆', '̵̧̡͕̜̱͖̟̜͙̐̉̈̊͑̈́͐̈', '̷̨̛̛̝͚̥̱̟̘̹̽̌̆̈́͘', '̵̜̬̯͖̜̣̃͋͑̌̈̂̈́̔̎̕̚͝', '̴̢͓̟̓̍̈́̀̉̊̈́̉̽͌͠', '̷̧̦̜̗̥̲̠͚̮̋̅̎́̏̀̌͜']
##
##
##

# Main function
if __name__ == "__main__":

    # Check if the user passed a text as argument
    if len(sys.argv) < 2:
        print("You need to pass a text as argument")
        sys.exit(1)

    # Get text pass as arguments, get all arguments and join them
    text_to_parasite = ' '.join(sys.argv[1:])

    # Trim the text
    text_to_parasite = text_to_parasite.strip()

    # Split text character by character
    characters_to_parasite = list(text_to_parasite)

    # Parasited sequence
    characters_parasited = list()

    # For each character in the new characters list
    for i in range(len(characters_to_parasite)):
        # Get the current character
        character = characters_to_parasite[i]
        # Choose a random sequence from the parasited sequences list
        random_sequence = random.choice(PARASITES)
        # Contact character and random sequence
        characters_parasited.append(character+random_sequence)
    
    # Concatenate the characters parasited list
    text_parasited = ''.join(characters_parasited)

    # Print the text parasited
    print('')
    print('')
    print('')
    print('')
    print(text_parasited)
    print('')
    print('')
    print('')
    print('')