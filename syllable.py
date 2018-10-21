# syllable.py by Antonius Yonathan
# A program that splits an Indonesian word to its constituent syllables
# Written on October 20th 2018

import sys, itertools

VOWELS = 'aiueo1234('
CONSONANTS = 'bcdfghjklmnpqrstvwxyz!#$%^/+=*,?'

DIPTHTONGS = {
    'ai': '1',
    'au': '2',
    'ei': '3',
    'oi': '4'
}

REVERSE_DIPHTONGS = {
    '1': 'ai',
    '2': 'au',
    '3': 'ei',
    '4': 'oi'
}

COMPOSITES = {
    'kh': '!',
    'ng': '#',
    'ny': '$',
    'sy': '%',
    'str': '?',
    'tr': '^',
    'pr': '/',
    'th': '+',
    'kr': '=',
    'sw': '*',
    'fr': ',',
    'e\'': '('
}

REVERSE_COMPOSITES = {
    '!': 'kh',
    '#': 'ng',
    '$': 'ny',
    '%': 'sy',
    '?': 'str',
    '^': 'tr',
    '/': 'pr',
    '+': 'th',
    '=': 'kr',
    '*': 'sw',
    ',': 'fr',
    '(': 'e\''
}

NO_DIPHTONGS = ["main", "lain"]

def preprocess(word):
    if word not in NO_DIPHTONGS:
        for diphtong, code in DIPTHTONGS.items():
            word = word.replace(diphtong, code)

    for consonant, code in COMPOSITES.items():
        word = word.replace(consonant, code)

    return word

def postprocess(syllables):

    result = []
    for syllable in syllables:
        for code, diphtong in REVERSE_DIPHTONGS.items():
            syllable = syllable.replace(code, diphtong)

        for code, consonant in REVERSE_COMPOSITES.items():
            syllable = syllable.replace(code, consonant)

        result.append(syllable)

    return result

#
# Two consecutive vowels breaks a word
# Ex: bu-ah, ta-at, sa-at
#

def split_by_consecutive_vowels(part):
    result = []
    temp = ""
    
    for i, char in enumerate(part):

        temp += char

        if (i + 1 >= len(part)):
            result.append(temp)
            break
        
        if (part[i] in VOWELS and part[i + 1] in VOWELS):
            result.append(temp)
            temp = ""

    return result

#
# A consonant between two vocales breaks a word
# Ex: a-pa-kah, i-tu-lah
#

def split_by_vowel_between_consonants(part):
    result = []
    
    start_pos = 0
    
    for i, _ in enumerate(part):

        if (i + 2 >= len(part)):
            result.append(part[start_pos:len(part)])
            break
        
        if (part[i] in VOWELS and part[i + 1] in CONSONANTS and part[i + 2] in VOWELS):
            result.append(part[start_pos:i + 1])
            start_pos = i + 1

    return result

#
# Two consecutive consonants breaks a word
# Ex: lang-geng, peng-gal
#

def split_by_consecutive_consonants(part):
    result = []
    temp = ""
    
    for i, char in enumerate(part):

        temp += char

        if (i + 1 >= len(part)):
            result.append(temp)
            break
        
        if (part[i] in CONSONANTS and part[i + 1] in CONSONANTS):
            result.append(temp)
            temp = ""

    return result

def split_into_syllabes(word):

    word = preprocess(word)

    result = [word]
    result = list(itertools.chain(*[split_by_consecutive_vowels(part) for part in result]))
    result = list(itertools.chain(*[split_by_consecutive_consonants(part) for part in result]))
    result = list(itertools.chain(*[split_by_vowel_between_consonants(part) for part in result]))
    result = postprocess(result)

    return result

if __name__ == "__main__":
    print(split_into_syllabes(sys.argv[1]))