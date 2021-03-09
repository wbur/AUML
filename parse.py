#!/usr/bin/env python3

import re, os, platform
from data import Data
import sys
import pyperclip

use_quotes = '-q' in sys.argv
append_commas = '-c' in sys.argv

data = Data()

intents = data.intents
variables = data.variables

intent_list = list(intents.keys())
limit = len(intents)
prompt = "Pick an intent [1-" + str(limit) + "]\n"
for i in range(limit):
    prompt = prompt + str(i+1) + ") " + intent_list[i] + "\n"

choice = int(input(prompt)) - 1

sentences = intents[intent_list[choice]]

if type(sentences) == str:
    sentences = [sentences]

all_utterances = []
for sentence in sentences:

    for key in variables:
        sentence = sentence.replace('$' + key, variables[key])

    #pieces = AUML.split(' ')
    # see https://stackoverflow.com/questions/9644784/splitting-on-spaces-except-between-certain-characters
    pieces = re.split(r"\s+(?=[^()]*(?:\(|$))", sentence)
    utterances = [[]]

    for piece in pieces:
        if piece[0] == '(' and piece[-1] == ')':
            fragments = piece[1:-1].split('|')
            new_utterances = []
            for index, utterance in enumerate(utterances):
                original_utterance = utterances[index]
                for fragment in fragments:
                    #use copy of original_utterance or it all goes to hell
                    new_utterance = list(original_utterance)
                    new_utterance.append(fragment)
                    new_utterances.append(new_utterance)
            utterances = new_utterances
        elif piece[-1] == '?':
            word = piece[0:-1]
            temp = []
            for index, utterance in enumerate(utterances):
                # keep the pattern WITHOUT the optional word
                temp.append(list(utterances[index]))
                # but also add the optional word to another branch
                utterances[index].append(word)   
            utterances.extend(temp)
        else:
            for index, utterance in enumerate(utterances):
                utterances[index].append(piece)
    all_utterances.extend(utterances)

all_utterances = [' '.join(x) for x in all_utterances]

list_set = set(all_utterances) 
# convert the set to the list 
unique_list = (list(list_set))

print ('***********************************')
print ('***********************************')
print ('Creating ' + str(len(all_utterances)) + ' utterances')
print ('***********************************')
print ('***********************************')

clip = ''
for utterance in unique_list:
    quote = '"' if use_quotes else ''
    comma = ',' if append_commas else ''

    fmt_utterance = quote + utterance + quote + comma
    print (fmt_utterance)
    clip = clip + fmt_utterance + "\r"

# all the utterances will be inserted
# into your clipboard
pyperclip.copy(clip)