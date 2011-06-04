#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Un petit script pour distinguer des motifs
# dans des séries.
#
# le fichier doit être un ensemble de valeurs,
# avec une valeur par ligne.

import os, sys
import math

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

def ecart_type(l):
	return int(math.sqrt(variance(l)))

def pente(l):
	return (l[-1] - l[0]) / (len(l))

def pente_reg_lin(l):
	# calcul de la pente en utilisant la méthode de régression
	# linéaire d'excel. voir :
	# http://office.microsoft.com/fr-ca/excel-help/pente-HP005209264.aspx
	_x = int(len(l) / 2) # car les valeurs sont linéaires
	_y = mediane(l)
	
	num = 0
	for i, y in enumerate(l):
		num += (i - _x) * (y - _y)
	
	den = 0
	for j in range(len(l)):
		den += (j - _x) ** 2
	
	return num / den

def pente_davinson(l):
	# l'équation de calcul de la pente qu'a utilisée davinson
	# je passe n = len(l)

def critere(prev_e, e):
	# Ceci est le critère, qui permet de classer des élements
	# selon qu'ils appartiennent à la liste ou pas.
	return (abs(mediane(prev_e) - mediane(e)) <= 500 and abs(ecart_type(prev_e) - ecart_type(e)) <= 50) 

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
			d = {}
			d["vmoyenne"] = mediane(e)
			d["vecart"] = ecart_type(e)
			d["vpente"] = pente_reg_lin(e)
			
			if d["vmoyenne"] > 4000:
				d["moyenne"] = "elevé"
			elif d["vmoyenne"] > 2000:
				d["moyenne"] = "moyenne"
			else:
				d["moyenne"] = "faible"

			if d["vecart"] > 300:
				d["ecart"] = "elevé"
			elif d["vecart"] > 100:
				d["ecart"] = "moyen"
			else:
				d["ecart"] = "faible"

			
			ret.append([e, d])
			prev_e = e

	return ret	

if __name__ == "__main__":
	 for e in process_input(read_file(sys.argv[1])):
	 	print e
		print ""
