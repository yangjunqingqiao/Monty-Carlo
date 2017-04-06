# !/usr/bin/env python2
# -*- coding: utf-8 -*-
# !/bin/sh

#  markov-crypto.py

import numpy as np
import string

# alphabet = \
# ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
# 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

alphabet = list(string.ascii_lowercase)
alphabet.append(' ')

alp_size = len(alphabet)

# You may want to appropriately rename 'text.txt'
f = open('plain-text-moby-dick-2.txt', 'r')

all_text = f.read()
all_letters = list(all_text)

# STEP 1: count consecutive letters for every pair of letters in the alphabet

count_pairs = {}
for i in alphabet:
    for j in alphabet:
        count_pairs[(i, j)] = 0

for i in range(len(all_letters)-1):
    if all_letters[i] in alphabet and all_letters[i+1] in alphabet:
        count_pairs[(all_letters[i], all_letters[i+1])] += 1

# STEP 2: construct a transition matrix (frequency matrix) using the counts above

prob_pairs = {}
for x in alphabet:
    total = float(0.0)
    for y in alphabet:
        total += count_pairs[(x, y)]
    for y in alphabet:
        prob_pairs[(x, y)] = float(count_pairs[(x, y)])/float(total)

# freq_matrix = np.random.ranf([alp_size, alp_size])
# add code here


# As a related exercise, you may try to find the most common consecutive-letter pair in a given text.

# Some text to which you could apply the functions in this script:
# text = 'the brown dog jumped over the red cat and that was really cool you see what i mean'
# Or you may try using the raw_input() function to prompt the user to input text,
# e.g., text=raw_inupt('Enter some text:').


# STEP 3: Define a function to encrypt a given text using a given permutation (to have something that you can decode).
# It should return encrypted text (as some kind of object).  You can create random permutations in numpy; see below.
# Try also defining the inverse "decrypt" to this "encrypt" function.

def encrypt(text, permutation):
    encrypted_text = ""
    # add code here
    for char in text:
        if char in alphabet:
            if char == ' ':
                encrypted_text += alphabet[permutation[26]]
            else:
                encrypted_text += alphabet[permutation[ord(char) - 97]]
    # you can use += to add to a string too (not just integers)
    return encrypted_text

# def decrypt(en_text, perm):
# the inverse function to encypt
# decrypt is not strictly needed, as long as you have one function that applies a permutation of the alphabet to some
# input text


# STEP 4: Define a function to compute the plausibility--or score--of a permutation for a given encrypted text and a
# given transition matrix (frequency matrix).

def score_function(permutation, encrypted_text):
    # add code here
    log_score = float(1.0)
    decryption = encrypt(encrypted_text, permutation)
    # add code here
    for char in range(len(decryption) - 1):
        if decryption[char] in alphabet and decryption[char+1] in alphabet:
            log_score += np.log(1 + prob_pairs[(decryption[char], decryption[char+1])])
    # add code here
    return log_score


# PERMUATIONS: some code to illustrate how to permutations work in numpy
identity = [i for i in range(alp_size)]
print "identity permutation", identity
print

perm = np.random.permutation(alp_size)
print "random permutation", list(perm)


def swap(permutation):
    new_perm = list(permutation)
    i1 = np.random.randint(27)
    i2 = np.random.randint(27)
    while i1 == i2:
        i1 = np.random.randint(27)
    new_perm[i1] = permutation[i2]
    new_perm[i2] = permutation[i1]
    return new_perm
# LAST STEP: Define a function that takes as input encrypted text and a number of iterations and returns the result of
# the Monte Carlo algorithm discussed in class (and in Diaconis' paper) to the encrypted text.  It should return text
# (as some kind of object.


def climb_algorithm(encrypted_text, iteration):
    permutation = perm
    old_score = score_function(permutation, encrypted_text)
    # add code here
    for r in range(iteration):
        print old_score
        new_permutation = swap(permutation)
        new_score = score_function(new_permutation, encrypted_text)
        if np.random.ranf() < (new_score/old_score)**300:  # try changing the exponent
            permutation = new_permutation
            old_score = new_score
    # add code here
    return permutation

encrypt_text = list(open('encrypted-text.txt', 'r').read())


iter_str = raw_input('Enter number of iterations:')
iterations = int(iter_str)
best = climb_algorithm(encrypt_text, iterations)

# best =  climb_algorithm(encrypt_text, 3000)  # play with the number of iterations

print "I think this is the permutation:"
print list(best)
print
print "and this is the decoded text:"
print
print encrypt(encrypt_text, best)


# I had a lot of fun with this writing assignment. In the end, I had to manually set a stopping point for the
# score to get a comprehensible decrypted message (I didn't include it in the code because it is specific only to this
# specific text file (which was something about Cleveland and baseball). I didn't get all the letters mapped but this is
# pretty close: [18, 22, 4, 6, 7, 12, 15, 11, 9, 24, 14, 2, 5, 8, 17, 16, 23, 21, 10, 3, 26, 20, 1, 0, 13, 25, 19].
# It definitely feels like this algorithm could be drastically improved because I had to run it multiple times on very
# large iterations to even get the score to a decently high value. I don't doubt the convergence of the algorithm but
# it converges very slowly for certain starting permutations. Either that or the drop-off at certain local maxima is
# incredibly steep.
