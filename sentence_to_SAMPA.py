import sys
# Project-local imports
from suku import pecah
from phoneme import malay_phoneme_types, syllable_to_phonemes, get_phoneme_type, duration_constants, durations

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz 's"

def calculate_duration(constant, d_i, d_min):
    return constant * (d_i - d_min) + d_min

def convert_phonemes(phonemes):
    phoneme_type = get_phoneme_type(phonemes)

    result = []
    for i, phoneme in enumerate(phonemes):
        
        constant = duration_constants[phoneme][phoneme_type[i]]
        d_i = durations[phoneme]['Di']
        d_min = durations[phoneme]['Dmin']

        result.append({
            'phoneme': phoneme,
            'type': phoneme_type[i],
            'duration': calculate_duration(constant, d_i, d_min)
        })

    return result


if (len(sys.argv) < 2):
    print("Cara penggunaan: ")
    print("python3 sentence_to_SAMPA.py \"Kalimat yang hendak diproses.\"")
    quit()

sentence = sys.argv[1]

# Lowercase input sentence
sentence = [letter.lower() for letter in sentence]

# Remove punctuations
sentence = [letter for letter in sentence if letter in ALLOWED_CHARACTERS]
sentence = "".join(sentence)

# Tokenize sentence
sentence = sentence.split(" ")

# Split each word in sentence into syllables
sentence = [pecah(word) for word in sentence]

# Break each syllable into its constituent phonemes
sentence = [[syllable_to_phonemes(syllable) for syllable in syllables] for syllables in sentence]

# Convert each phoneme into a dictionary containing it and its type
sentence = [[convert_phonemes(phonemes) for phonemes in word] for word in sentence]

for word in sentence:
    for syllable in word:
        for phoneme in syllable:
            print(phoneme)



