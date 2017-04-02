# !/usr/bin/env python2
# -*- coding: utf-8 -*-
# !/bin/sh

#  markov-crypto.py

import numpy as np
import random

alphabet = ['a', 'b', 'c', 'd', ' e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', ' ']

alp_size = len(alphabet)

# You may want to appropriately rename 'text.txt'
f = open('plain-text-moby-dick-2.txt', 'r')
# print f
# f.readline()

all_text = f.read()
text_as_letters = list(all_text)

# for i in range(50):
#    print all_letters[i],

# STEP 1: count consecutive letters for every pair of letters in the alphabet


# add code here
def count_pairs(all_letters):
    matrix = np.zeros((27, 27))
    for x in range(len(all_letters) - 1):
        if ord(all_letters[x]) == 32 and ord(all_letters[x + 1]) == 32:
            matrix[26][26] += 1
        elif ord(all_letters[x]) == 32:
            matrix[26][ord(all_letters[x + 1]) - 97] += 1
        elif ord(all_letters[x + 1]) == 32:
            matrix[ord(all_letters[x]) - 97][26] += 1
        else:
            matrix[ord(all_letters[x]) - 97][ord(all_letters[x + 1]) - 97] += 1
    return matrix

# STEP 2: construct a transition matrix (frequency matrix) using the counts above

freq_matrix = np.random.ranf([alp_size, alp_size])
# add code here


def construct_trans(matrix):
    new_mat = matrix
    for x in range(26):
        s = 0
        for y in range(26):
            s += count_pairs(text_as_letters)[x][y]
        for y in range(26):
            new_mat[x][y] = matrix[x][y]/s
    # # changing 0s
    # for x in range(26):
    #     for y in range(26):
    #         if new_mat[x][y] == 0:
    #             new_mat[x][y] = 0.0001
    # finding most common pairing
    big = 0
    row = 0
    col = 0
    for x in range(26):
        for y in range(26):
            if big < new_mat[x][y]:
                big = new_mat[x][y]
                row = x
                col = y
    print row, col
    return new_mat

# As a related exercise, you may try to find the most common consecutive-letter pair in a given text.

# Some text to which you could apply the functions in this script:
# text = 'the brown dog jumped over the red cat and that was really cool you see what i mean'
# Or you may try using the raw_input() function to prompt the user to input text,
# e.g., text=raw_input('Enter some text:').


# STEP 3: Define a function to encrypt a given text using a given permutation (to have something that you can decode).
# It should return encrypted text (as some kind of object).  You can create random permutations in numpy; see below.
# Try also defining the inverse "decrypt" to this "encrypt" function.

def encrypt(text, perm):
    new_text = ""
    for char in text:
        if ord(char) - 97 > 25 or ord(char) - 97 < 0 and ord(char) != 32:
            continue
        elif ord(char) == 32:
            new_text += alphabet[perm[26]]
        else:
            new_text += alphabet[perm[ord(char) - 97]]
    return new_text
# add code here


def decrypt(en_text, perm):
    new_text = ""
    for char in en_text:
        if ord(char) - 97 > 25 or ord(char) - 97 < 0 and ord(char) != 32:
            continue
        elif ord(char) == 32:
            new_text += alphabet[perm[26]]
        else:
            new_text += alphabet[perm[ord(char) - 97]]
    return new_text
# the inverse function to encypt


# STEP 4: Define a function to compute the plausibility--or score--of a permutation for a given encrypted text
# and a given transition matrix (frequency matrix).

def score_function(permutation, trans_matrix, encrypted_text):
    new_text = decrypt(encrypted_text, permutation)
    frequency_matrix = count_pairs(list(new_text))
    prob = 1
    for c in range(26):
        for r in range(26):
            prob *= trans_matrix[c][r]**frequency_matrix[c][r]
    return prob

# PERMUATIONS: some code to illustrate how to permutations work in numpy
permutation = [i for i in range(alp_size)]
print "identity permutation", permutation
print

perm = np.random.permutation(alp_size)
print "random permutation", list(perm)


# LAST STEP: Define a function that takes as input encrypted text and a number of iterations and returns the result of
# the Monte Carlo algorithm discussed in class (and in Diaconis' paper) to the encrypted text.  It should return text
# (as some kind of object).


def climb_algorithm(encrypt_text, iters):
    trans_matrix = construct_trans(count_pairs(text_as_letters))
    old_permutation = list(perm)
    old_score = score_function(old_permutation, trans_matrix, encrypt_text)
    for i in range(iters):
        i1, i2 = random.sample(list(permutation), 2)
        new_permutation = old_permutation
        temp = new_permutation[i1]
        new_permutation[i1] = new_permutation[i2]
        new_permutation[i2] = temp
        new_score = score_function(new_permutation, trans_matrix, encrypt_text)
        if random.uniform(0, 1) <= np.divide(new_score, old_score):
            old_permutation = new_permutation
            old_score = new_score
    return old_permutation

encrypt_text = list(open('example.txt', 'r').read())
best = climb_algorithm(encrypt_text, 5000)  # play with the number of iterations

print "I think this is the permutation:"
print list(best)
print
print "and this is the decoded text:"
print
print encrypt(encrypt_text, best)

# I had thought this program was going to be fast and easy but I did not give myself enough time to work on the program.
# I believe the reason my code will not produce a coherent unencrypted text is because my method of choosing new
# permutations is incorrect. I did not handle the 0 cases in the matrix correctly and I did not adapt the random walk
# algorithm correctly. 
