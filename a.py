"""
Assignment:	Project 3
Members:	Trevor Fox
Date:		12/06/16
Assignment:	Given a context-free grammar G, this program
		generates a leftmost derivation for a given 
		string w by a recursive search if one exists 
		within k steps. If such a k-step derivation 
		does not exist, it returns false.
"""

import sys
import re
from collections import defaultdict
import random

class CFG(object):
	
	def __init__(self):
		self.prod = defaultdict(list)
		self.win = 'S=>'
		self.count = 0
		self.current = ''
	
	def add_prod(self, lhs, rhs):
		""" Add production to the grammar. 'rhs' can be several productions 
		separated by '|'. Each production is a sequence of symbols separated 
		by whitespace. """
		prods = rhs.split('|')
		for prod in prods:
			self.prod[lhs].append(tuple(prod.split()))

	def winString(self, rule):
		# store current rule, print.
		# on next iteration:
		# search the rule, replace instances of CAPITAL letters with the new rule
		if self.count < 1:
			self.current = rule
		else:
			for c in self.current:
				if c.isupper():
					self.current = self.current.replace(c, rule)
		self.win = self.win+self.current+'=>'
		self.count = self.count + 1

	def clearWinString(self):
		self.win = 'S=>'
		self.count = 0
		self.current = ''

	def gen_random(self, symbol):
		""" Generate a random sentence from the grammar, starting with the given symbol. """
		sentence = ''
		# select one production of this symbol randomly
		rand_prod = random.choice(self.prod[symbol])
		# prints the production rules
		self.winString(str(rand_prod).replace(',','').replace('\'','').replace('\)','').replace('\(','').replace(' ',''))
		for sym in rand_prod:
			# for non-terminals, recurse
			if sym in self.prod:
				sentence += self.gen_random(sym)
			else:	sentence += sym + ' '
		return sentence
	
def main():

	# Create Context Free Grammar class object
	cfg1 = CFG()

	counter = 0
	f = open(sys.argv[1])
	for line in iter(f):
		if counter > 2:
			first = str(line[0])
			sec = str(line[2:].rstrip())
			sec = (" ".join(sec))
			cfg1.add_prod(first, sec)
		counter += 1
	f.close()

	# ask user for input string and k
	w = raw_input("Enter string: ")
	w = (" ".join(w))+" "
	k = raw_input("Enter k: ")

	res = cfg1.gen_random('S')
	# return true or false
	for i in range(0, 50000):
		if str(w) == res:
			break	
		cfg1.clearWinString()
		res = cfg1.gen_random('S')
	
	if str(w) == res:
		print str(cfg1.win+res).replace(' ','').replace('(','').replace(')','')
	else:
		print "false"

if __name__ == "__main__":
	main()

