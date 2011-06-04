#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Un petit script pour distinguer des motifs
# dans des séries.
#
# le fichier doit être un ensemble de valeurs,
# avec une valeur par ligne.

import os, sys
import math
import genmidi

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

def critere(prev_e, e):
	# Ceci est le critère, qui permet de classer des élements
	# selon qu'ils appartiennent à la liste ou pas.
	return (abs(mediane(prev_e) - mediane(e)) <= 5 and abs(ecart_type(prev_e + e) <= 3)) 

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
	#	print "e : %s, prev_e : %s" % (e, prev_e)
		if critere(prev_e, e):
			prev_e += e
			# prev_e = e
		else:
			# rajoute les caractéristiques finales de la section
			# à la fin, avant de rajouter le tout à la fin de la
			# liste retournée.
			d = {}
			d["vmoyenne"] = mediane(prev_e)
			d["vecart"] = ecart_type(prev_e)
			d["vpente"] = pente_reg_lin(prev_e)
			
			if d["vmoyenne"] > 106:
				d["moyenne"] = "elevé"
			elif d["vmoyenne"] > 95:
				d["moyenne"] = "moyenne"
			else:
				d["moyenne"] = "faible"

			if d["vecart"] > 2.6:
				d["ecart"] = "elevé"
			elif d["vecart"] > 1:
				d["ecart"] = "moyen"
			else:
				d["ecart"] = "faible"

			if d["vpente"] > 1.1:
				d["pente"] = "elevé"
			elif d["vpente"] >= 0:
				d["pente"] = "moyen"
			else:
				d["pente"] = "faible"

			
			ret.append([prev_e, d])
			prev_e = e

	return ret	

if __name__ == "__main__":
	l = process_input(read_file(sys.argv[1]))
	del l[0] # Enlève un déchet qui est là je ne sais pas
		# trop pourquoi
	genmidi.generate_drum_track(l, "out.mid")
