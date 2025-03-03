#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parasite Text Generator

This script adds visual "parasites" (special Unicode characters) to text,
creating a glitched or corrupted appearance while preserving readability.
The original characters remain, but each is followed by distortion elements.
"""

import random
import sys
import argparse
from typing import List, Tuple


# Parasite sequences - Unicode combining characters that visually distort text
PARASITES = ['̶̬̯̻̾͊͂', '̵̜͔̭̃̈́͂̑̑̓͌̐̋̂̚̚͘͝͠', '̴̻̜͖̘̹͙̭̙͇̻̈́́̚', '̵̢̦͇̐̃̋̈́͗͂̓̇̈͛̅̏̕͝͝', '̴̞͈͓͐̓̎͋̚͝', '̶̨̡͙͙̞̖͇̩̖͚̙͇̹͔̘̃͛̉', '̶̣̠̙̑͋̿͑̈́̉̀̀̈́͌͛̈̏̀̄', '̶̫̱̥̟̤̺͔̯̱͚͛̾̾̿͘ͅ', '̷̮̺̜̘̯͉͕͕͚̾̿͊̃̚͜͝͠', '̷̛̬͚̳̗͓͓̹̫͙͋̄̀̀͗̓̈́', '̴̠͓̤̣̟͙͓̬̗̊̾̈́̀̈́̈́̀̎̕', '̷̝̖͍̗͍̪̯̼̯̻͋̈', '̸̢̠̜̱͈͍̄̉͑̕͠͝', '̷̠̳̠̳̞̇̔', '̴̖̟͙͎̱̓͐̋̕', '̴̢̨̢̺̩̤͇̟̲̄̌̂̕', '̸̞̦̘̠̼͎͖̬̘͌̎͐̓͒̚͘͝ͅ', '̴̥́̉́̉̅̌̓̍́͑̽̚̚', '̸̼͎̜͎͎͂͒̓͑̈́͒̓̕͘͜͜͝͠', '̸͖̌̕͝͝', '̵̧̲̤̬͛̎͋̏͂̎̉͊́͒̈̽̚̕', '̴̯̟̜͎̆͆̽̊͌̅̏̀̓̇̋̚͠͠', '̵̡̧̧̫̦̥̫͚͉͕̺̐̈́̌͋̔͒̈', '̴͖̘͚̩̮̩̹̮̹̀̈́́͌̾͗̓͠͝', '̵̧̣̝̩̲̮̘̳͇̔̂̀͑́̐́̇͜', '̷̛̛̛͕͉̺̓̀̀̽̅̇̊͋̄̿̈́̀', '̸̡̛͚̰̭̼̹͍̎̄̄͘͘̚', '̶̦͇̬̰̒̌͆̂̐̌̈́͆͋̎̀', '̴͚̗̏̑͛̋̈̀̇̒̓̈́͆̍̽', '̶̨͔̺̱͙̪̳̬̺̭̦̒̾̅̄̕̚͜', '̶̢̧͈͇̝̝̰̖͍̅͠͠', '̴̮́͌', '̴̞̀̽̈́', '̴̧̟̞̞̜̖̬͕͈̳͈͕̯̣̇̎', '̷̢̛̣̣͙̋̚', '̶͍͇̪̿', '̵̭̆̽̒̅̊̋̈́̐́̆͘', '̷̫͙͇͕́̔͊͑̐͘͠', '̸̢̡͎̙̮̻̻̼̬̬̇͆͛̆̈̒͘͠', '̷̥͍͓͍͛͌͆̐̐̀͑̀̆̉͐̕͘͠', '̸͕̟̣̩̽̉͋̈̈́͑̕͝͠', '̵̗̠̑̐', '̶̳̘͓̪̯̀̇̈́͌̿̿̂͘͠ͅ', '̶̡̧̨̤̺̬̣̤͕̺̖͓̬͗͑͒́ͅ', '̴̧̧̩͓͇̜͚́̃̍̆́̄͗͗͛̆', '̵̧̡͕̜̱͖̟̜͙̐̉̈̊͑̈́͐̈', '̷̨̛̛̝͚̥̱̟̘̹̽̌̆̈́͘', '̵̜̬̯͖̜̣̃͋͑̌̈̂̈́̔̎̕̚͝', '̴̢͓̟̓̍̈́̀̉̊̈́̉̽͌͠', '̷̧̦̜̗̥̲̠͚̮̋̅̎́̏̀̌͜']

# Categorized parasites by visual intensity
LIGHT_PARASITES = ['̴̮́͌', '̴̞̀̽̈́', '̵̗̠̑̐', '̶͍͇̪̿', '̷̠̳̠̳̞̇̔', '̸͖̌̕͝͝']
MEDIUM_PARASITES = ['̶̬̯̻̾͊͂', '̴̞͈͓͐̓̎͋̚͝', '̴̖̟͙͎̱̓͐̋̕', '̷̝̖͍̗͍̪̯̼̯̻͋̈', '̵̭̆̽̒̅̊̋̈́̐́̆͘']
HEAVY_PARASITES = ['̵̜͔̭̃̈́͂̑̑̓͌̐̋̂̚̚͘͝͠', '̶̨̡͙͙̞̖͇̩̖͚̙͇̹͔̘̃͛̉', '̶̣̠̙̑͋̿͑̈́̉̀̀̈́͌͛̈̏̀̄', '̸̼͎̜͎͎͂͒̓͑̈́͒̓̕͘͜͜͝͠', '̵̧̲̤̬͛̎͋̏͂̎̉͊́͒̈̽̚̕']


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Add visual "parasites" to text to create a glitched appearance.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        %(prog)s "Hello World"                    # Basic usage
        %(prog)s -f input.txt                     # Read from file
        %(prog)s -i heavy -d 0.8 "Corrupted text" # Heavy corruption with 80% density
        %(prog)s -c "aeiou" "Vowels only"         # Only corrupt vowels
        """
    )
    
    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('text', nargs='*', help='Text to parasitize', default=[])
    input_group.add_argument('-f', '--file', help='Read text from file')
    
    # Parasite configuration
    parser.add_argument('-i', '--intensity', choices=['light', 'medium', 'heavy', 'random'], 
                        default='random', help='Intensity of parasites (default: random)')
    parser.add_argument('-d', '--density', type=float, default=1.0,
                        help='Probability (0.0-1.0) of adding parasites to each character (default: 1.0)')
    parser.add_argument('-c', '--characters', 
                        help='Only parasitize specific characters (e.g., "aeiou" for vowels only)')
    
    # Output configuration
    parser.add_argument('-n', '--no-padding', action='store_true',
                        help='Remove empty lines before and after output')
    parser.add_argument('-o', '--output', help='Write output to file instead of stdout')
    parser.add_argument('-s', '--seed', type=int, help='Random seed for reproducible results')
    
    return parser.parse_args()


def get_input_text(args: argparse.Namespace) -> str:
    """Get input text from either command line arguments or a file."""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            sys.exit(f"Error reading file: {e}")
    else:
        return ' '.join(args.text).strip()


def get_parasite_set(intensity: str) -> List[str]:
    """Get the appropriate set of parasite sequences based on intensity."""
    if intensity == 'light':
        return LIGHT_PARASITES
    elif intensity == 'medium':
        return MEDIUM_PARASITES
    elif intensity == 'heavy':
        return HEAVY_PARASITES
    else:  # random
        return PARASITES


def parasitize_text(text: str, args: argparse.Namespace) -> str:
    """Add parasite sequences to the input text based on configuration."""
    # Get the appropriate set of parasites
    parasites = get_parasite_set(args.intensity)
    
    # Convert text to list of characters
    characters = list(text)
    result = []
    
    # Process each character
    for char in characters:
        # Check if we should parasitize this character
        should_parasitize = (
            (not args.characters or char in args.characters) and 
            random.random() < args.density and
            not char.isspace()  # Don't parasitize whitespace
        )
        
        if should_parasitize:
            # Choose a random parasite sequence
            parasite = random.choice(parasites)
            result.append(char + parasite)
        else:
            result.append(char)
    
    return ''.join(result)


def output_result(text: str, args: argparse.Namespace) -> None:
    """Output the parasitized text to stdout or a file."""
    # Prepare the output with or without padding
    if args.no_padding:
        output = text
    else:
        output = '\n\n\n\n' + text + '\n\n\n\n'
    
    # Output to file or stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output written to {args.output}")
        except Exception as e:
            sys.exit(f"Error writing to file: {e}")
    else:
        print(output)


def main() -> None:
    """Main function to process arguments and parasitize text."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
    
    # Get input text
    text = get_input_text(args)
    
    # Validate input
    if not text:
        sys.exit("Error: Input text is empty")
    
    # Parasitize the text
    parasitized_text = parasitize_text(text, args)
    
    # Output the result
    output_result(parasitized_text, args)


if __name__ == "__main__":
    main()