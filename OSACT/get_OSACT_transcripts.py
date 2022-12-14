from dataclasses import replace
import argparse
import re
import csv
import random
import time
from googletrans import Translator # pip install googletrans==3.1.0a0
from emot.emo_unicode import UNICODE_EMOJI, EMOTICONS_EMO, UNICODE_EMOJI_ALIAS

parser = argparse.ArgumentParser()
parser.add_argument('--XYtrain_path', type=str) # path to training data + labels
parser.add_argument('--Xtest_path', type=str)   # path to test data
parser.add_argument('--Ytest_path', type=str)   # path to test labels
args = parser.parse_args()

OSACT_XYTRAIN_PATH = args.XYtrain_path  # '/Users/lilykawaoto/Documents/GitHub/LING-L715/OSACT/OSACT_train.csv'
OSACT_XTEST_PATH = args.Xtest_path      # '/Users/lilykawaoto/Documents/GitHub/LING-L715/OSACT/OSACT2020-sharedTask-CodaLab-Train-Dev-Test/OSACT2020-sharedTask-test-tweets.txt'
OSACT_YTEST_PATH = args.Ytest_path      # '/Users/lilykawaoto/Documents/GitHub/LING-L715/OSACT/OSACT2020-sharedTask-CodaLab-Train-Dev-Test/OSACT2020-sharedTask-test-taskB-gold-labels.txt'

def remove_emojis(txt):     # helper for preprocess()
    translator= Translator()
    text = ""
    for char in txt: 
        if char in UNICODE_EMOJI or char in UNICODE_EMOJI_ALIAS or char in EMOTICONS_EMO:
            continue
        else:
            text += char
    return text


def preprocess(txt):
    patterns = ['#', '@', 'USER', ':', ';', 'RT', 'URL', '<LF>', '\.\.\.', '…', '!', '\.', '\?', '%', '\*', '"', "'", '\$', '\&', '/', '\)', '\(', '\[', '\]', '\}', '\{', '|', '\d+']
    text = re.sub('|'.join(patterns), '', txt)          # remove patterns
    text = re.sub(r'[a-zA-Z]', '', text)                # remove non-Arabic characters
    text = re.sub(r'\t', ' ', text)                     # replace tabs with single space
    text = re.sub(r'(.)\1\1+', r'\1', text)             # remove 3 or more repetitions of any character
    text = remove_emojis(text)                          # remove emojis and emoticons
    return text

"""
Read in csv file. Preprocess each tweet as it's being read in. 
Store cleaned text plus its label in a tsv file.
"""

""" TRAINING FILE"""
with open(OSACT_XYTRAIN_PATH, 'r') as f:
    osact_train_list = []
    reader = csv.reader(f, delimiter=",")
    for i,row in enumerate(reader): 
        row = [nonspace for nonspace in row if nonspace]
        
        # For some reason, some of these rows result in either 1 or 3 columns. To be investigated further.
        if (len(row) != 2):
            if len(row)==1:
                row = row[0].split('\t')
                print(f"New row: {row}\n")
                if len(row)!=3:
                    continue
                osact_train_list.append((preprocess(row[0]), row[2]))
            elif len(row)==3:
                row = ' '.join(row)
                row = row[0].split('\t')
                print(f"New row: {row}\n")
                if len(row)!=3:
                    continue
                osact_train_list.append((preprocess(row[0]), row[2]))
        
        else:
            osact_train_list.append((preprocess(row[0]), row[1].strip()))

### TO-DO: add argparse argument for name of this file
with open('osact_train_cleaned.tsv', 'w') as f:
    for pair in osact_train_list:
        f.write(f"{pair[0]}\t{pair[1]}\n")


""" TEST FILES (TXT & LABELS) """
with open(OSACT_XTEST_PATH, 'r') as f1, open(OSACT_YTEST_PATH, 'r') as f2:
    reader1 = f1.read().splitlines() 
    reader2 = f2.read().splitlines()
    osact_test_list = [(preprocess(row), reader2[i]) for i,row in enumerate(reader1)]  

### TO-DO: add argparse argument for name of this file
with open('osact_test_cleaned.tsv', 'w') as f:
    for pair in osact_test_list:
        f.write(f"{pair[0]}\t{pair[1]}\n")