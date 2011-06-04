#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Un petit script pour distinguer des motifs
# dans des séries.
#
# le fichier doit être un ensemble de valeurs,
# avec une valeur par ligne.

import os, sys

def read_file(fname):

	try:
		fd = open(fname)
	except IOError:
		print "unable to open requested file."
		sys.exit(-1)

	ret = []

	lines = fd.readlines()
	for line in lines:
		ret.append(int(float(line))) # moche mais de toutes façons, avec
					     # toutes les moyennes que l'on fait
					     # la précision est balancée de toutes
					     # façons.


	fd.close()
	return ret

def mediane(l):
	# Calcule la médiane d'une liste.
	div = len(l)
	acc = 0

	for e in l:
		acc += e

	return acc / div

def variance(l):
	div = len(l)
	acc = 0
	med = mediane(l)

	for e in l:
		acc += (e - med)**2
	
	return acc / div

def critere(prev_e, e):
	# Ceci est le critère, qui permet de classer des élements
	# selon qu'ils appartiennent à la liste ou pas.
	return abs(mediane(prev_e) - mediane(e)) <= 2

def process_input(l):
	l1 = []
	ret = []
	# D'abord, casser la liste en plusieurs parties dont on calcule la variance et l'espérance
	for i in range(len(l) / 2):
		t = [l.pop(0), l.pop(0)]
		l1.append(t)
	
	# Ensuite calcule les médianes et variances de chaque élements et fusionne les élements contigus
	# qui sont proches.
	prev_e = l1[0] # l'élement précedent
	ret.append(prev_e)
	
	for e in l1[1:]:
		# TODO: définir un seuil correct - avec de vrais critères.
		if critere(prev_e, e):
			prev_e += e
			prev_e = e
		else:
			# rajoute les caractéristiques finales de la section
			# à la fin.

			d = {"type": "moyen", "moyenne" : mediane(e), "variance" : variance(e) }
			ret.append([e, d])
			prev_e = e

	return ret	

if __name__ == "__main__":
	 for e in process_input(read_file(sys.argv[1])):
	 	print e
		print ""
