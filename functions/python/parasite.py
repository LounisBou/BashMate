#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Parasite Text Generator

This script creates visually corrupted text using Unicode combining characters
and other special characters. The output text maintains readability while
appearing distorted, glitched, or "infected" with visual parasites.
"""

import random
import sys
import argparse
import math
from typing import List, Tuple, Dict, Callable
import string
import unicodedata

# ============================
# PARASITE CHARACTER LIBRARIES
# ============================

# Basic combining diacritical marks
BASIC_PARASITES = ['̶̬̯̻̾͊͂', '̵̜͔̭̃̈́͂̑̑̓͌̐̋̂̚̚͘͝͠', '̴̻̜͖̘̹͙̭̙͇̻̈́́̚', '̵̢̦͇̐̃̋̈́͗͂̓̇̈͛̅̏̕͝͝', '̴̞͈͓͐̓̎͋̚͝', '̶̨̡͙͙̞̖͇̩̖͚̙͇̹͔̘̃͛̉', '̶̣̠̙̑͋̿͑̈́̉̀̀̈́͌͛̈̏̀̄', '̶̫̱̥̟̤̺͔̯̱͚͛̾̾̿͘ͅ', '̷̮̺̜̘̯͉͕͕͚̾̿͊̃̚͜͝͠', '̷̛̬͚̳̗͓͓̹̫͙͋̄̀̀͗̓̈́', '̴̠͓̤̣̟͙͓̬̗̊̾̈́̀̈́̈́̀̎̕', '̷̝̖͍̗͍̪̯̼̯̻͋̈', '̸̢̠̜̱͈͍̄̉͑̕͠͝', '̷̠̳̠̳̞̇̔', '̴̖̟͙͎̱̓͐̋̕', '̴̢̨̢̺̩̤͇̟̲̄̌̂̕', '̸̞̦̘̠̼͎͖̬̘͌̎͐̓͒̚͘͝ͅ', '̴̥́̉́̉̅̌̓̍́͑̽̚̚', '̸̼͎̜͎͎͂͒̓͑̈́͒̓̕͘͜͜͝͠', '̸͖̌̕͝͝', '̵̧̲̤̬͛̎͋̏͂̎̉͊́͒̈̽̚̕', '̴̯̟̜͎̆͆̽̊͌̅̏̀̓̇̋̚͠͠', '̵̡̧̧̫̦̥̫͚͉͕̺̐̈́̌͋̔͒̈', '̴͖̘͚̩̮̩̹̮̹̀̈́́͌̾͗̓͠͝', '̵̧̣̝̩̲̮̘̳͇̔̂̀͑́̐́̇͜', '̷̛̛̛͕͉̺̓̀̀̽̅̇̊͋̄̿̈́̀', '̸̡̛͚̰̭̼̹͍̎̄̄͘͘̚', '̶̦͇̬̰̒̌͆̂̐̌̈́͆͋̎̀', '̴͚̗̏̑͛̋̈̀̇̒̓̈́͆̍̽', '̶̨͔̺̱͙̪̳̬̺̭̦̒̾̅̄̕̚͜', '̶̢̧͈͇̝̝̰̖͍̅͠͠', '̴̮́͌', '̴̞̀̽̈́', '̴̧̟̞̞̜̖̬͕͈̳͈͕̯̣̇̎', '̷̢̛̣̣͙̋̚', '̶͍͇̪̿', '̵̭̆̽̒̅̊̋̈́̐́̆͘', '̷̫͙͇͕́̔͊͑̐͘͠', '̸̢̡͎̙̮̻̻̼̬̬̇͆͛̆̈̒͘͠', '̷̥͍͓͍͛͌͆̐̐̀͑̀̆̉͐̕͘͠', '̸͕̟̣̩̽̉͋̈̈́͑̕͝͠', '̵̗̠̑̐', '̶̳̘͓̪̯̀̇̈́͌̿̿̂͘͠ͅ', '̶̡̧̨̤̺̬̣̤͕̺̖͓̬͗͑͒́ͅ', '̴̧̧̩͓͇̜͚́̃̍̆́̄͗͗͛̆', '̵̧̡͕̜̱͖̟̜͙̐̉̈̊͑̈́͐̈', '̷̨̛̛̝͚̥̱̟̘̹̽̌̆̈́͘', '̵̜̬̯͖̜̣̃͋͑̌̈̂̈́̔̎̕̚͝', '̴̢͓̟̓̍̈́̀̉̊̈́̉̽͌͠', '̷̧̦̜̗̥̲̠͚̮̋̅̎́̏̀̌͜']

# Extended combining marks for more varied effects
EXTENDED_COMBINING = [
    # Combining diacritical marks
    '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306', '\u0307', '\u0308', '\u0309', 
    '\u030A', '\u030B', '\u030C', '\u030D', '\u030E', '\u030F', '\u0310', '\u0311', '\u0312', '\u0313',
    '\u0314', '\u0315', '\u0316', '\u0317', '\u0318', '\u0319', '\u031A', '\u031B', '\u031C', '\u031D',
    '\u031E', '\u031F', '\u0320', '\u0321', '\u0322', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327',
    '\u0328', '\u0329', '\u032A', '\u032B', '\u032C', '\u032D', '\u032E', '\u032F', '\u0330', '\u0331',
    '\u0332', '\u0333', '\u0334', '\u0335', '\u0336', '\u0337', '\u0338', '\u0339', '\u033A', '\u033B',
    '\u033C', '\u033D', '\u033E', '\u033F', '\u0340', '\u0341', '\u0342', '\u0343', '\u0344', '\u0345',
    '\u0346', '\u0347', '\u0348', '\u0349', '\u034A', '\u034B', '\u034C', '\u034D', '\u034E', '\u034F',
    
    # Combining diacritical marks for symbols
    '\u20D0', '\u20D1', '\u20D2', '\u20D3', '\u20D4', '\u20D5', '\u20D6', '\u20D7', '\u20D8', '\u20D9',
    '\u20DA', '\u20DB', '\u20DC', '\u20DD', '\u20DE', '\u20DF', '\u20E0', '\u20E1', '\u20E2', '\u20E3',
    '\u20E4', '\u20E5', '\u20E6', '\u20E7', '\u20E8', '\u20E9', '\u20EA', '\u20EB', '\u20EC', '\u20ED',
    '\u20EE', '\u20EF',
    
    # Combining half marks
    '\uFE20', '\uFE21', '\uFE22', '\uFE23', '\uFE24', '\uFE25', '\uFE26', '\uFE27', '\uFE28', '\uFE29',
    '\uFE2A', '\uFE2B', '\uFE2C', '\uFE2D', '\uFE2E', '\uFE2F'
]

# Special character transformations
GLITCH_CHARS = [
    '҉', '̸', '̷', '̵', '̶', 'ඞ', 'ත', 'ꙮ', '꙰', '⃝', '⃠', '⃟', '⃢', '⃤', '█', '▓', '▒', '░', '▄', '▀',
    '■', '□', '▪', '▫', '●', '○', '◆', '◇', '◊', '✕', '✖', '✗', '✘', '☒', '☓', '✓', '✔', '☑',
    '⌧', '⍰', '⎔', '⎕', '⏣', '⌗', '⌘', '⏥', '⏢', '⎈'
]

# Zero-width characters
ZERO_WIDTH = [
    '\u200B', '\u200C', '\u200D', '\u200E', '\u200F', '\uFEFF', '\u2060', '\u2061', '\u2062', '\u2063', '\u2064',
    '\u2065', '\u2066', '\u2067', '\u2068', '\u2069'
]

# Create themed parasite sets
THEMES = {
    "classic": BASIC_PARASITES,
    
    "digital": [
        '█̷͓̽', '░̶͚̆', '▒̸̡̃', '▓̶̱͂', '■̸͕͠', '□̴̺̚', '▢̵̩̐', '▣̵̘̈́', '▤̷̬̊', '▥̵̛̯', '▦̸̥̓',
        '▧̴͇̇', '▨̸̟̆', '▩̵̢̑', '▪̸̻͊', '▫̷̞̕', '▬̸̣̽', '▭̶̣̍', '▮̶̟̓', '▯̸̥̀', '▰̸̡̂', '▱̷͓̔',
        '▲̴̯͝', '△̸̡̏', '▴̶̤͘', '▵̶̲̈', '▶̸̡̐', '▷̶̥̔', '▸̴̬̽', '▹̴̩̾', '►̷̺̚', '▻̵̤̑', '▼̵̧̃',
        '▽̴̠̓', '▾̸̝̓', '▿̵̼͝', '◀̵̪̽', '◁̵̥̾', '◂̷̫̎', '◃̷̼̓', '◄̵͙̌', '◅̸̤̃',
    ],
    
    "cursed": [
        'ꙮ̵̭̿', '꙰̷̘̀', '⊗̵̢̾', '⊙̵̢̐', 'ᨛ̴̻̎', 'ඞ̸̧͝', 'ඣ̶̔ͅ', 'ඥ̵̞̋', 'ඩ̵̘͊', 'ඬ̸̡̄', 'ච̷̃ͅ',
        'ත̶̦̾', 'ᯓ̸͐͜', 'ᨒ̴̗̑', '҉̵̢̈́', '☠̵̱̽', '☢̸̭̏', '☣̵̨̂', '⍾̷̮̑', '꩜̷̢̓', '⚠̵̛̬',
    ],
    
    "matrix": [
        '0̵̡̀1̷̣̇', '1̵̥̐0̸̫̈́', 'ㄖ̸̳̒', 'ㄗ̵͇͊', 'ﾉ̸̺̒', 'ﾌ̸̬̂', 'ﾓ̶̗̆', 'ﾑ̷̟͠', 'ﾘ̶̧̂', 'ﾚ̵̻̏', 'ﾛ̶̱͂',
        '力̵͇͊', '刀̶̫̇', '乃̵͚̔', '口̶̹́', '尺̵̗̎', '乇̷̡͐', '下̸̖̃', 'ㄚ̴͕͂', 'ㄒ̷̻̓', 'ㄩ̶̲̍',
    ],
    
    "ancient": [
        '𓀀̷͙̃', '𓀁̷̥͛', '𓀂̴̜͘', '𓀃̶̲͂', '𓀄̵̥̓', '𓀅̸̹̔', '𓀆̶̼̾', '𓀇̵̮͒', '𓀈̶̫͗', '𓀉̶̗̉',
        '𓀊̷͙̊', '𓀋̸̥̂', '𓀌̶̤̀', '𓀍̵̦̊', '𓀎̴̛͜', '𓀏̴̭̑', '𓀐̵̪̚', '𓀑̸̡̐', '𓀒̷̙͂', '𓀓̴̪̈',
        '𓆣̵̢̿', '𓆤̶̖̋', '𓆥̷̬̄', '𓆦̸̥͐', '𓆧̵̺̊', '𓆨̶̹͌', '𓆩̵̱̚', '𓆪̵̧̉', '𓆫̶̦́', '𓆬̷̫̈',
    ],
    
    "vaporwave": [
        'ｖ̵̨̓ａ̸̳̌ｐ̴̱͂ｏ̸̟̕ｒ̸̬̀', 'ｗ̶̗̀ａ̵̲͐ｖ̸̤̍ｅ̷̝͊', 'ａ̵̙͌ｅ̸̪̍ｓ̸̱͌ｔ̶̹̒ｈ̵̬̓ｅ̸̥̒ｔ̶̨̽ｉ̴̕͜ｃ̵̖̍',
        'サ̶͓͂イ̴̨̕バ̵̜̄ー̶̺̉パ̵̮͠ン̵̙̀ク̴̫̽', 'ト̸̯͠リ̸̫̎ッ̶̗̿プ̴̫̊', 'コ̸̞̎ン̵̥͠ピ̴̯̌ュ̷̗̋ー̶̡̔タ̶̣̄',
        '夢̵̠̃', '幻̸̙̅', '想̸̬̂', '愛̵̝͝', '永̵̓ͅ', '遠̸̞͋', '郷̶̯͊', '愁̵̹̍', '懐̶͉̾', '海̵̛̘',
    ],
    
    "alien": [
        '̵̧̧̢̱͉̞̫̞̘͚̥̝̲͎͉̪̜̲̑̂̂͐̅̀̊̐͆͜͜͝', '̶̨̧̦̦̥̟̪̱͔͕̩̙͇̟̭̽̉̊̌̋̕͜͠͝ͅ',
        '̸̡̡̛̝̖͙̪̼̫͚͈̦̠͈̦̰̖̤̼̲̘̈́́̑͆̔̌̄̔̃͊̀̃̐̌̊̒̀̑͂͌̑͒͆̀̈͗̈́̕̚̕͘̚͜͜͝͝͝͠͝͠͝',
        '̴̡̢̨̡̡̨̡̢̧̧̧̢̨̛̛̛̛̖̖̥̜̦̜̤͖̺̮̗̣̱̰̺̲͚͕̭͔̠̫̤͖̠̺̪͕̠̪̭̹̞̝̥̻͍̥͓̼̠̹̟̦͉̼̝̯̲̫̝͈̼̫̲̖̭̠̹̜̞̣̤̼̯̳̯̹̝̭̲͚̻̘͍͍̤̦͎͉͈̠̮̦͚̞̦̘̘̤̜͇̫̞̣͚̮̻̞̅͆̀̄̄̍̌̓͐͛́͌̒̇͛̆͒͆͂̋̈͋̀̋̿̒̄̓̔̍͌̀̂̄͗̃̈́̄̈̓̓̽̇̋̊͐̒̄̽͐́̀͛̿̑̓̽̀̑̽̇̎̓̀̓͑͑̍̽̾̋̈́͆͋̈́̏̈́͊̌̇̋̄͊͌͑̿͋̈́̍͑̇͌̀̍͛̈́̽͋̈̽͒̿̊̍̈́̊̃̿͆̂̃̾̌͗̒̋̎̄͗͌̊̆̚̕̚̕̚̕̚͜͜͝͝͝͝͝͠͝͠͝͝͝ͅͅͅͅͅ',
        '̸̨̡̡̨̛̛̫̫̜̩̣̞̬̭̘̼̱̦͓͙͓͓͕̰̮̤̬̙͉̪͔̹̖̰̜͚͕̦̤̼̙̝̤͉̤̮͇̻̜̦̩̬͔͇̇̋̓̽͗͆̊̽̄̐͂͗̒̔͐̇͒̓̿̅̔̔͗̓̈́̒̌̽̀̔͐̃̏̀͑̾̍̄̅̽̐̆́̽̓̀̎̽̍̓͂͂͆̈́̐̅͋̆͂͆͘̚̚̚̚̕͘̚͜͝͝͠ͅͅͅ',
        '̸̢̡̡̡̧̨̧̧̛̣̲̫̯̹̣̯̺̭̦͇̞̪̱̥͕̫͓̗̱̰̼̞̰̮͔̮͓̙͔̮̫̱̭̯̻̗̣̪̼̣̲̘̼̞͕̝̤̻̣̺̤̭̬̳̱̰̱̪̫̝̺̱͉͇̮̞̙̦̟̲̼͔̦̙̥̝̣̮̯͕͔̭͋̀̓̊͋̂͌̃̊̈̔̒̓͂̐̆̈́̊̓̒̿̌̒͆́̿̽̿͗̇͑̄̿͋͌͒͂̈́̍̓̂͒͗̐̆̈͒͆͆͆̾̀̑̾͋̄̀̐͊̽͐͐̈̑͑̀̈̔̑̊͆̿̽̌̄̑̋̔̂̀̆̀̅̋̅̅̊̃̐̓͛̄͑̃̊̈́͋̎̎͂̂̏̾͑̉͑̾͑̏͌̇̒̏̀̒̏̍̑́̾̋͆̅̽̓́̈́̈́̓̀͌̀̈́̽̂̎͂̒̈̌̈́̀̔̈͑̈̈́̋̄̿̋̎̀̇͒͐̀̂̅̽͊͐̿̀͗̔̽̄̂͛̃̕͘̚̚͘̚̚̕̕͘̚̕̕̚͘̚̚͘͜͜͝͠͝͝͝͝͝͠͝͝͝͝͝͝͠͝͝ͅͅͅ',
    ],
    
    "zalgo": [
        # Stacked combining marks for extreme effects
        "z̴͇̃a̸̗̓l̵̝̾g̵̟̑ỏ̴̙", "z̶̛̘̙̳̖̣̦̫̯̙̝̾́̈́͗͝ͅa̷̭̖̱̣̹̘̜̙̾͊͋̏̃͐͆̿l̴̡̪͈̩̦̞̮̺͗͑̓̀̌̑͠g̷̭̬̀͆͐̏͒͂̀̀̕ó̵̻̬͓̦̥̥͋͒̐̌̕", 
        "z̴̞̉̍̓͂ā̵̡̙͓͠l̸̨̞̭̙̅͋͑g̶̹̥̒͆͑ö̴͍̣́̋", 
        "ź̷̢̡̡̧̡̨̢̛̛̹͇̦͔̱͖̰̻̫̳̟̗͙͍͍̠̥͇̞̞̟̯̖̟̤̺͚̝̙̮̱̩̦̬̘͖̘̤̜̤̼̻͔̱̼̰͈̫̪̻̝̟̘̣̥̭̹̝̼͍̻̬̣̫̗̻̘̪̯̳̭̳̥̬̤̙͇̣̼̺̼͖͍͓̯̳̠̘̝̩̱̼̬̲̫͈̠͉͓͂̒̀̀̃̿̅̒͗̈̓̀̾̓́̓̀͒̄̈́̓̾͐͐̽̂͌͑͐̇͋͂̃̈͐̓̌̎͛̎̓̒́̊̇̋͂͌͑̆̓̈́̉͑̃̒͋͌̓͌̔͂̓̓̔͆͋̑͛̅̉̏̿̌̐̔̑̋̈́̉̚̚̕̚̚̚͝͝͝͝͝ͅͅͅͅͅa̶̢̢̛̛̛̛̝̟̘͇̩͍̦̬͓̼͍̭̲̬͖͚̯͎̠̟̰͚̱̜̻̳̟̦̹̗̯̯̟̜̩͖̺̯̭̰̯̥̩͈̰̤̪̣̮̖̘̗̺̳̦̻̤̪̰̰̝̱͔̙̜̙̭̻̱̱̻̗͕̟̻̠̫̟̗̬̼͖͙̘̩̪̳̙͊͌̒̎̈́͗̌̆̾̌̔͐̊͋̔͐̇̆̓̓͑̏̓͆̈́̏̅̓̊̂̏̍͐̉͋͊̓̀͗͆͌̄̌̂͗͗̉͂̓̔̈́͐̒̀̾͂̓͒͂̾̒̽̆̂̉̊͌̃̀̈̒̓͑̏͛̒͂̉̀̀͂̏͂̐̇̀̑̊͛̀̅͋̉̐͑͑̊̍̋̔͗̐͒̓̊͆̑̀́̑̉̏̀͒̈́͛̃͋̈́̈́̈̐͛̋͛̀̾̀̈́͗̓͒́͐̊̆̑̅͗̐̂̏̋̍̽̇̽͋̚̕̕̚̕̚͘̚̕̕̚̚͜͜͜͝͝͠͠͝͝͝͠ͅͅl̴̡̧̢̢̨̢̧̡̢̛̛̮̥̹̱̞̺̬̭̲̹̬̙̗͙̥̣̠̠̹̹̭̜̦̦̞̣̤̭̮̻̼̬̯̭̪̘̻̫̯̝̹̮̻̣̙̙̲͎̤͎̯̙̼̯̣̱̫̼̜̰̭̣̫̗̫͎̪̗̦̰̮̭̰̥̩̺̠̺̙̮̝̝̱̲̝͔͙͓̥̱̥̳̰̱̹͕̫̥̪̜̲͔̬̬̯̘͎̫̺̳̲̪̼̭̩̻͈̲̟̫̰̹̳̮̙̪͚̦͓̱̗̥͇̫̬̙͙͕̤̠̗̜̣̱̻̯̙̥̣̗̮̝͉̮͎̣̱͕̗̰̝̩͕̣̮̰̪̦̰̝̼̫̘̃̓̓̀͐̂́͌̄͊̋̊̈́́͑͊̓̈̋̏͆̌̉̆̓̇̀̀̆̍͆̃̐̓́̓̑̾̀̉̌̈́̓̉̌̒̑̄̇͛͂͂̓͐̃͛͛͗͋͆̋̈́̆̐̑̍̇̐͒̃͐̊̅͆̈́͂̑̏́̇̎͊̋͋͋̚̚̚̕̚̚͜͜͠͝͝͠͝͝ͅͅͅͅģ̸̧̛̛̛̫̭̻̯̦̳̠̞͈̰̗̩̳͇̬̮̱̹͔̩̰͇̘͔̝̣̜̪͉̗̜͎̘̯͖̪̫̗̮̺͍̌̀̈̓̃͛̈́͆̈͗̃̋̎̍̔͗̆͆̄̉̂̀̓̋̈́͋̍͋̌͛͆͌́͋͌̆̓̌̇̍͒͋̋̈́̿̀̐̎͒̃̀̐͗̂̽̈́̽̃̔̐͒͛͒̀̀̽͗̈̓͌͗̿̈́̌̆̽̐̌̿̆̔͒͒͗̽̅̃̔̏̔͑̒̿͂͌̿̋̄͊̎̒̑̏̏̋̂͆͛̊͛͗̿̔̓̽̈́̾̑̄̆͐͑͒̏͋̀̿̅̅͑͂̂̾̆̉̋̊̾̓̚̚͘̚̕̚̕͝͠͝͝͠͝͝͝ǫ̸̨̨̧̡̨̡̡̡̧̨̡̧̧̨̧̨̛̛̛̛̛̫̭̞̘̤͖̤̳͓̪̭͔̭͇͇̦̬̤̮̮̥̝̜̣̬̝̦͖̝̩͙̘̘̩̻̱̪̣̙̭̞̫͔͖̜̙̜̗͎̹̞̬̙̥̪̭͔̖̰͚̜̜̬̗̦̞͍̣̯̖̙̪͍̙̫̟̗̖̭̥̬̙̤̭̰̻̯̟̬̬̪̲̠̘͙̜̥̖̫̗̯̻̞̝̠͎̻̘̭̦̰͓̗̹̲̦̮̲̭͇̺̠̳̬̤̰͖̥͓̞̰͚̖̻̙͚̻̲̳̣͙̤̜̙̻̓̔͗̏͆͆͋̍̈́̿̏͂̋̀̽̎̈́͊͊͊̑̒͆̍͆̀̃͊͆̽̾̀̽̀̓̀̀̓̓̂͑̓̏̀̓͆́̀́̇̇̄̅̆̆̃̌̍̈́̇͌̇́͊̈̐͒͐̎̉̔̾̇̇͆̃̍̆̃̀̈͊̃̄́̾͐͂̋̊̐̿̎͛̀̉͒̾̋̆̐̄̄̅̄̂̓̐̏̅͂͒͆̓̇̿͆͊̓͊͋͂͗̊̀̑͘̕͘̕͘̚̚͘̚̚̚̚͜͜͜͜͜͜͝͝͠͝͝͝͝͝͝͝͝ͅͅͅͅ"
    ],
    
    "cthulhu": [
        "p̵͎̙̪̜̤̤̰͎̗̗̟̋̾̓̓́͒̌̓̍͐̈́̾̈́̒̈́̑̽̀̏̿͌̚̚͜͝͝h̸̡̨̡̝͚̙̠͖̬̫̝̤̺̱͇͔̬͕̙̗̠̹̭̤̹̘̖̲̰̞̗̿͑͊̈́̓͌̌͘̚̚͝'̵̡̨̧̯͉̱̣͎̠̯͕̭͚̜̯̪̪̰͕̝͔͚͎̲̭͗̎̑̈̉̽͛̈̊̂̃̃̃͊͒̌̏́͂̐̓̚͜͝͠ͅṇ̴̨̛̖̤̞̤̯̦̦̰̗̦̼̺͉͚̗̞̠̤͚̲̰͕̜̭̩͈͍̹̯̟͍͖̗̘͖͍̥̬̥͖̪̣̮͉̬̝̬̪͐̃̈́͑̽͊͐̅̏̏̈́͆͗̈́̌̀̌͐̓̌̌̾̏͐̇̈́̇͐̔̈́̈́̽̂̅̾͛̒̕͜͠͝͝ͅͅg̸̨̡̡̧̢̧̺̱͕̙̪̣̼̠̠̥̤̟̖̱̣̠̘͉͎̯̟̞͇͙͍͈̲͎̪̲̙̫̩̤̜̠̥̹̼͋̏͛͂̍̿̄͘͜͜͜ͅͅͅl̸̡̨̛͉͇̮̘̖̭̩̗̤͇̻̘̘̪̠̮̖̼̭̲̮͖̩̀̽̀̀͐̅́̍̈́̆͐̿̑̎͊̔́̽̃̅̍̚͘͝ų̷̨̢̧̛͈̰̯̯̬̹̫͔̫̫̙̥͔̞̫̼̪̱͎̹̩̟̞̤̲̗̜̣̝̱̙̳̹̳̣̮̦̩̞̦̑͊̍̓̇̃̋͜ͅi̶̧̡̢̛͎̮͈̲̙͚͉̼̙̦̱̙̙̬͔̯̩̰̠̹͕̥̩̪̫̫̣̠͔̥̘̙̿̓͊̈́̂̀͑̊̀̐́̓͐̍̓͑̕͘͘͜͜͝ͅͅͅ ̶̨̛̛̜̖̭̪̺̙͈̩̗̻̮̘̮̭̭̭̈́̋̌̀͒̓̀̾͋̍͒̉̉̀̉̉̈́͌̊̌͑̏͑͒̓̄̓͒̃̈̊̆̅̆̕̚̚͠͝͠m̸̛̜̰̞̻̉̀̀̉͗̒͌̊̒̓͋̒̓̊̓̿̎͘͝g̶̛̙̩̠̗̠̝̃̀͂̿̆̃̈́͊͊͊̏́̄̅͗̐͆͋̀͗̀́̽̽̀̈́̓̏̚͝͝ļ̵̨̨̧̪̗̱̝͔̲̤̞̫̼̣̰̝̥̭̩̞̏̆̅̉̈́̍̋̔͋̔̒͛͌͜͝w̶̛̹̰̥̗̬͔͓̪̦̹̭̯̾̓̃̆͘ͅ'̶̡̨̢̛̩̫̺͎̤̻̪̯̗̱͕̫̻̜̪̠̙̦̲̟̺̺̟̹̤̆͂̋̍̅͌̈̂́̅̐̈͆͐̾͛̅̐̏̀̉̌͋̈́̔͂̉̈̾͌͘̚͝ͅͅn̷̢̘̬̥͙̦͙̊̋̀̍̊̋͒͛̂̓̽͊̐̉̒̈̌͗̈́̐̏̈́͊̽͌͝͝͠ą̴̢̥̣̳̟̞̤̦̮̠͕͕͎̱̝͓͙̹̼͇͉̰̰̖͕̥̥͕̬̼͕̠̙͙̳͋̔̎͛̆̂̽͛̆̑̈́̊͊͐̍̈̔͊̎͒̄́͑̈̈́̈̓̄̐̍̉̾͒̈́̑͑̈́̋̓̂͘͘͠͝͝͝͝f̴̨̧̛̫̙̙̗̪̜͉̤̼̭̤̰̼̱̞͓̥̳̠͈͎̮͍̪̠̰̫̠̣̯̝̃̈́̒̀̌̇̏̐̂̓̂͑̑͊̈̈́̾̏͋́̏̕̚̕̕͝͝ĥ̶̢̢̨͙̩̙̩̬̰̫̿̒̊̽͌̽̆̓̿̌̑͒̌̊̇͐̀͂̄̈̎͌́̌͜ͅ ̶̧̡̢̧̡̤̝̝̘͓̗̦͓͖͎̻̘̞̻͖͓̙̭̖̬̭̘̥̯̄̿̆̾̔͒̆́̅̐̒́̂̓̐͊̾̆̀́͘̚͜͠͝ͅͅ",
        "R̷̨̛̹͇̜̫̪̉̎̀̒͑̄̾̄̂̎̃͂̂̑̂̀̄͂̐̓̎̍͑̄̀̾̃̂̎̈̈́̂͘̚͜͝͠'̸̡̢̧̹̪̣̙̺̟̥̲̹̟̯̹̺̰͕̤̝͙͇̭̺̰͚̜̻̝̩͖̜͓̺̓̈̌̄͒̀́̐ḽ̸̙̥̤̭̘̙̗̖̦͓̘̰̍̓̉̓̏̓ỳ̸̧̛̙̖̯͖̯̹͍͖̜̯̣̱̥̜̦̺̹̭̰̰͓̽̽̌̌̅͛̈̋̀̅̃̓̄̿̑̾̇͌̊̑̓͘̕͜͝͝ͅe̸̛̛̮̱̠̝̙̞̟͕̠͂̈́̏͒̎̑̄̐̍̚h̸̢̛͈̹̬̼̽̽͂͗͊̑͌̓͌͊͂̾͋̓̄͑̃̌̊͋̀͋̽̾̇̇̽̒͊̔̓̔͒̓̕͘͝͝",
        "C̷̨̨̡̠̫̱̣̝̦͕̫̥͎͔̘̯̙̺̪͇̰͍̯̬̣̈̎̏̽̾͆̽͋̎̿̽̄͐̎͑̑̚̚͜͝t̵̢̢̧̧̢̛̥̫̜̗̮̯͇̱̭̬̥̞͕̠̭̰̬̺͖̣̜̝̬̯̯̠̤͔̦͍̝̰̣̙̬̙̥͔̭̝̦̰͈̻̘̗͍̲̬̻̤̳̫̺̝̮̠͓̱̞͔͓͎̑̓̇̇͗̍͑͋͛͋̈́̽̏̈́̋̓̔̀̈̅̇̓̅̀͋̊́͐̾̊̓͛͒͛̉́̎͛͊͘̚̚̚͜͜͜͝͠͠͝ͅẖ̵̡̨̢̡̧̧̡̡̡̨̢̧̛̘̻̞̪̹̲̮̪̰̱̠̞̱̥̦̥̮͚͖̯̱̬̥̙̦̪̖̱̥̮͎͉̪̞̱̠̥̗̖͔̫̭̪̤̱̤̰̫̟̖̙̮͙̥͕̗̝̦̼̬̙̹̘̟͖͍͖̲͙͙̽̋̓̇̎̋̄̄̅̌̍̃̓͆͂̏̃̉̃̀̎̆̑̂̿͒̃̉̽̑͐̎̑͊̐͑̏̄̒̉̏̔͑̉̂̐͗̃̌̾͛̂̋͘͘̕͘͘͘͜͜͝͠͝͝ͅͅͅư̸̢̹̬̙̠͔̼̰̙̻̟̫̖̯̯̟̹̼̲̟̺̝̥̠̲̣̜̹̙͓̱̳̠̞̬̩̆̓̽͑͑͊̇̃͊̈́͗̄͂͆͗̈͆̒͊̓̓̒̐̉͌̈́͛̑̈̂̌̃̈́̕͜͜͠͝͝͠ͅͅͅl̵̨̧̧̛̲̟͍̺̲̪̝̟̪̮̹͈̗̯̯̹̥̮̝̣͙̫̳̩̣̹̖̬̤͙̼̠̭̀̋̈́̓̆͗̌̋̋̀̌͛̑̀̎̇̂̌̋̀͆́̊̀̋̓̈́̀̍͑͑͛̔̋͋̑͑̊͆͒̏̏̾͐̆̑̔̄̐̆̓̓̀̀̌̑̎̉̂͋̾̎̊̚̚̕̕̕̚͘͜͜͝͝͝͝͝ͅh̷̢̢̧̨̢̖̭͓̦̬̼̲͙̫̜̞̠̬̟̞̖̼͕̘̖̫̱̻̳̝͓̻̮̮̘̩̠̦̮̝̦͈͔̳̩̠̱̞̺̻̼̣̖̗̲̪͓͈͉̘̻̝̝͈̰̜̗̪̱̤̖̤̮͚͈̗̐̎̌͆̐͐̉̾͆̾̂̎͌̈̋̐͗͐̃̊̾̈̈́̌͌͊͋̓̍͌̍̀̃̐̇̀̃̎̚̚͠͝ͅư̴̢̧̧̨̧̢̛̛̛̱̯͇̘̯̮̹̦̞̠̰͙̤̱̦̪̣̟̘̠̰̝̟̘͙̪̖͓͙̲̘̠͕̬̟̹̞̺̱̫̖̻̠͚̦̝̓̾̇̐̓͌̋͊̑̒͛͒̂͋͒̇̍̀̏̿̄̄̌̏̀̈́̇̒̎̿̽̽̄̋̌̓͊́̌̒̑̽̐́̎̽̄̾̏̏͊̓̌̋͊͆͑̄̿̀̾͘̚̚̕͠͝͝͝͠ ̸̡̨̼̯̗̬̺̪̹̯͚̣̗͎̘̣̳̗̬̦̳͕̘̩͚̥̬̩̺̫̮̔̇̊̆͜͜ͅf̸̗̗̹̗̖̼͕̽̀̎͐̽̑̀͌̿̽́̋͐͘͠ḫ̶̛̥̠̪͎͈̰͉̟̭̖͉̪͓̫̬̽̽̎̆̊͊̿͆̌̐̎̈̔̈́̋̐͊̓͂̃̾̆̏̍̅̎̂͂̈͒͘͜͝͠͝t̵̨̧̢̡̧̡̨̧̧̢̧̤̰̼̙̤̰̫̯̳̻̫̥̟̫̙̲̪͎̬̦̖̹̣̩̣̫͖̮̞̘̙̙̤̞̦̬̻̘̪̹̰̭̥̪̩̙̹͉̬̪̬̜̩̒́̇̎̔̈́̑̊̅̎̾͌̌̌̇̑̑͌̚͜͜͜͜͝ͅͅa̶̡̛̛̛̠̭̮̞̙̞̩̠̟̱̺͔̦̙̞̙̗̦̤̬̺̻̯̘͖̻͇͈̳̠̥̺̰̝̗͇̤͎̯̥̪̖͓̩̱̤̞͔͈̳̗̮̪̣̙̫̖̩̗̳̤̘͛̀̓̅̒͌̒͆͒͂̍̃͐͋͂̒̀͑͗̅̆͌̎̀͐̌͆̋̀̃̊̀̐͑̅̒̋̌͌̈́͆̂̊̚̕̕͜͝͝ģ̸̨̡̡̧̧̨̛̛̛̛͍̠͚̤̪̹̥̲̜̤̯̣̺̩̞̯̯̜̤̗̥̱̭̬͇̳̗̤̟͕̝̼̘̜̲̲̙̔̌́̿̀͗̀́͗̈́̈́͆̇̓͗͛͐̍̓̐͐͑̏̀̓̈́͂̓̋̿̉̐͂̓͐͑̄̓̆͛̐̆̿̾͊̎̈́͌̌̓͆͛̿̍͊͊̾̓̈́̆̿̄̍̒̈́̈̍̾́͋͛̃̓̌̚̚̚̕̕͘͝͝͝͠͝͝͝͠͠ͅͅņ̵̨̡̨̨̡̡̧̳̬̮̱̥̯̭̣̯̦̠͉̭̝̳̦̖̬̜̹̞̙͇̠̬̖̹̰̪̩̖̫̪̲͚̜̜̬̣̬̮͒̑͂̎̔̓̑̎̓́̾̉̈͊̊̽̀̐̀̓̿̊͗̂̌͊̈́͂̈́̄̓͌̽̌̔̋̉̔̊͋̚͘͝͝͝͝ͅ",
    ]
}

# Function prototypes for different text effects
def wave_pattern(index: int, length: int) -> float:
    """Create a sine wave pattern based on character position."""
    return 0.5 + 0.5 * math.sin(2 * math.pi * index / (length / 3))

def gradient_increase(index: int, length: int) -> float:
    """Create an increasing gradient effect (start light, end heavy)."""
    return min(1.0, index / (length * 0.7))

def gradient_decrease(index: int, length: int) -> float:
    """Create a decreasing gradient effect (start heavy, end light)."""
    return max(0.0, 1.0 - (index / (length * 0.7)))

def middle_peak(index: int, length: int) -> float:
    """Create a peaked effect with highest intensity in the middle."""
    return 1.0 - (2.0 * abs(index - (length / 2)) / length)

def random_intensity(index: int, length: int) -> float:
    """Create random intensity fluctuations."""
    return random.random()


# Presets for different effect patterns
EFFECT_PATTERNS = {
    "uniform": lambda i, l: 1.0,
    "wave": wave_pattern,
    "gradient_in": gradient_increase,
    "gradient_out": gradient_decrease,
    "peak": middle_peak,
    "random": random_intensity,
}


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments with enhanced options."""
    parser = argparse.ArgumentParser(
        description='Advanced Parasite Text Generator - Create visually corrupted text with Unicode combining characters.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello World"                       # Basic usage
  %(prog)s -f input.txt                        # Read from file
  %(prog)s -t digital "Matrix text"            # Use digital theme
  %(prog)s -e wave -t zalgo "Wavy corruption"  # Apply wave effect with zalgo theme
  %(prog)s -m 3 "Multiple parasites per char"  # Apply multiple parasites per character
  %(prog)s --animation "Moving corruption"     # Create an animation-like effect
  %(prog)s --cthulhu "Ph'nglui mglw'nafh"     # Use the Cthulhu theme for eldritch text
  %(prog)s --transform vowels "Transform text" # Replace vowels with transformed versions
        """
    )
    
    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('text', nargs='*', help='Text to parasitize', default=[])
    input_group.add_argument('-f', '--file', help='Read text from file')
    
    # Basic configuration
    parser.add_argument('-t', '--theme', choices=list(THEMES.keys()), default='classic',
                        help='Theme of parasites to use (default: classic)')
    parser.add_argument('-e', '--effect', choices=list(EFFECT_PATTERNS.keys()), default='uniform',
                        help='Effect pattern to apply (default: uniform)')
    parser.add_argument('-d', '--density', type=float, default=1.0,
                        help='Base probability (0.0-1.0) of adding parasites to each character (default: 1.0)')
    
    # Advanced parasitizing options
    parser.add_argument('-m', '--multiplier', type=int, default=1,
                        help='Number of parasites to add per character (default: 1)')
    parser.add_argument('-c', '--characters', 
                        help='Only parasitize specific characters (e.g., "aeiou" for vowels only)')
    parser.add_argument('--animation', action='store_true',
                        help='Create an animation-like effect with varying parasites')
    parser.add_argument('--transform', choices=['none', 'all', 'vowels', 'consonants', 'random'], default='none',
                        help='Transform characters instead of just adding parasites')
    
    # Themed shortcuts
    parser.add_argument('--cthulhu', action='store_true', help='Use Cthulhu theme with heavy corruption')
    parser.add_argument('--zalgo', action='store_true', help='Use extremely corrupted Zalgo text')
    parser.add_argument('--matrix', action='store_true', help='Use Matrix-style digital corruption')
    parser.add_argument('--alien', action='store_true', help='Use alien language style corruption')
    parser.add_argument('--vaporwave', action='store_true', help='Use vaporwave aesthetic')
    
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


def get_parasite_set(args: argparse.Namespace) -> List[str]:
    """Get the appropriate set of parasite sequences based on theme and shortcuts."""
    # Handle themed shortcuts first
    if args.cthulhu:
        return THEMES["cthulhu"]
    elif args.zalgo:
        return THEMES["zalgo"]
    elif args.matrix:
        return THEMES["matrix"]
    elif args.alien:
        return THEMES["alien"]
    elif args.vaporwave:
        return THEMES["vaporwave"]
    
    # Otherwise use the selected theme
    return THEMES[args.theme]


def transform_character(char: str, transformation_type: str) -> str:
    """Transform characters based on the specified transformation type."""
    # Define character sets for transformations
    FULLWIDTH_MAP = str.maketrans(
        string.ascii_letters + string.digits + string.punctuation + ' ',
        ''.join(chr(ord(c) + 0xFEE0) if ' ' != c else chr(0x3000) for c in string.ascii_letters + string.digits + string.punctuation + ' ')
    )
    
    # Define specialty mappings
    SPECIALTY_MAPS = {
        'circled': {
            'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ', 'h': 'ⓗ', 'i': 'ⓘ', 'j': 'ⓙ',
            'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ', 'o': 'ⓞ', 'p': 'ⓟ', 'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ',
            'u': 'ⓤ', 'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ', 'y': 'ⓨ', 'z': 'ⓩ',
            'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 'F': 'Ⓕ', 'G': 'Ⓖ', 'H': 'Ⓗ', 'I': 'Ⓘ', 'J': 'Ⓙ',
            'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ', 'O': 'Ⓞ', 'P': 'Ⓟ', 'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ',
            'U': 'Ⓤ', 'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ', 'Y': 'Ⓨ', 'Z': 'Ⓩ',
            '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④', '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨'
        },
        'math_script': {
            'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ', 'h': '𝒽', 'i': '𝒾', 'j': '𝒿',
            'k': '𝓀', 'l': 'ℓ', 'm': '𝓂', 'n': '𝓃', 'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉',
            'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏',
            'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢', 'H': 'ℋ', 'I': 'ℐ', 'J': '𝒥',
            'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩', 'O': '𝒪', 'P': '𝒫', 'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯',
            'U': '𝒰', 'V': '𝒱', 'W': '𝒲', 'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵'
        },
        'small_caps': {
            'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
            'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ',
            'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
        }
    }

    # Check if we should transform this character
    is_vowel = char.lower() in 'aeiou'
    is_consonant = char.lower() in 'bcdfghjklmnpqrstvwxyz'
    
    if transformation_type == 'none' or char.isspace():
        return char
    elif transformation_type == 'all':
        pass  # Transform all characters
    elif transformation_type == 'vowels' and not is_vowel:
        return char
    elif transformation_type == 'consonants' and not is_consonant:
        return char
    elif transformation_type == 'random' and random.random() < 0.5:
        return char
    
    # Apply a transformation
    transformation_choice = random.choice(['fullwidth', 'circled', 'math_script', 'small_caps'])
    
    if transformation_choice == 'fullwidth':
        return char.translate(FULLWIDTH_MAP)
    else:
        # Use specialty maps for other transformations
        specialty_map = SPECIALTY_MAPS[transformation_choice]
        return specialty_map.get(char, char)


def parasitize_text(text: str, args: argparse.Namespace) -> str:
    """Add parasite sequences to the input text based on configuration."""
    # Get the appropriate set of parasites
    parasites = get_parasite_set(args)
    
    # Convert text to list of characters
    characters = list(text)
    text_length = len(characters)
    result = []
    
    # Get the effect pattern function
    effect_function = EFFECT_PATTERNS[args.effect]
    
    # Process each character
    for i, char in enumerate(characters):
        # Apply character transformation if enabled
        if args.transform != 'none':
            transformed_char = transform_character(char, args.transform)
        else:
            transformed_char = char
        
        # Calculate the effect intensity at this position
        effect_intensity = effect_function(i, text_length)
        
        # Adjust the density based on the effect intensity
        adjusted_density = args.density * effect_intensity
        
        # Check if we should parasitize this character
        should_parasitize = (
            (not args.characters or char in args.characters) and 
            random.random() < adjusted_density and
            not char.isspace()  # Don't parasitize whitespace
        )
        
        if should_parasitize:
            # Start with the transformed character
            parasitized_char = transformed_char
            
            # Add the specified number of parasites
            for _ in range(args.multiplier):
                # Choose parasites based on animation effect or randomly
                if args.animation:
                    # Create variation based on character position
                    parasite_index = (i * 3 + _ * 7) % len(parasites)
                    parasite = parasites[parasite_index]
                else:
                    parasite = random.choice(parasites)
                
                parasitized_char += parasite
            
            result.append(parasitized_char)
        else:
            result.append(transformed_char)
    
    return ''.join(result)


def create_demo_text() -> str:
    """Create a demonstration of various parasite effects for help text."""
    demos = []
    
    # Basic themes
    demos.append("THEME EXAMPLES:")
    for theme in ["classic", "digital", "cursed", "matrix", "ancient", "vaporwave", "zalgo", "cthulhu"]:
        args = argparse.Namespace()
        args.theme = theme
        args.effect = "uniform"
        args.density = 1.0
        args.multiplier = 1
        args.characters = None
        args.animation = False
        args.transform = "none"
        
        parasites = THEMES[theme]
        demo_text = f"Theme: {theme}"
        parasitized = parasitize_text(demo_text, args)
        demos.append(f"  {parasitized}")
    
    # Effect patterns
    demos.append("\nEFFECT PATTERNS:")
    for effect in ["uniform", "wave", "gradient_in", "gradient_out", "peak", "random"]:
        args = argparse.Namespace()
        args.theme = "classic"
        args.effect = effect
        args.density = 1.0
        args.multiplier = 1
        args.characters = None
        args.animation = False
        args.transform = "none"
        
        demo_text = f"Effect: {effect}"
        parasitized = parasitize_text(demo_text, args)
        demos.append(f"  {parasitized}")
    
    # Multiplier examples
    demos.append("\nMULTIPLIER EXAMPLES:")
    for multiplier in [1, 2, 3]:
        args = argparse.Namespace()
        args.theme = "classic"
        args.effect = "uniform"
        args.density = 1.0
        args.multiplier = multiplier
        args.characters = None
        args.animation = False
        args.transform = "none"
        
        demo_text = f"Multiplier: {multiplier}"
        parasitized = parasitize_text(demo_text, args)
        demos.append(f"  {parasitized}")
    
    # Animation and transform examples
    demos.append("\nSPECIAL EFFECTS:")
    special_configs = [
        {"name": "Animation", "animation": True, "transform": "none"},
        {"name": "Transform (vowels)", "animation": False, "transform": "vowels"},
        {"name": "Transform (all)", "animation": False, "transform": "all"},
    ]
    
    for config in special_configs:
        args = argparse.Namespace()
        args.theme = "classic"
        args.effect = "uniform"
        args.density = 1.0
        args.multiplier = 1
        args.characters = None
        args.animation = config["animation"]
        args.transform = config["transform"]
        
        demo_text = f"Effect: {config['name']}"
        parasitized = parasitize_text(demo_text, args)
        demos.append(f"  {parasitized}")
    
    return "\n".join(demos)


def output_result(text: str, args: argparse.Namespace) -> None:
    """Output the parasitized text to stdout or a file."""
    # Prepare the output with or without padding
    output = text

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
    # Special case for --help to show demo
    if "--help-demo" in sys.argv:
        print(create_demo_text())
        sys.exit(0)
    
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