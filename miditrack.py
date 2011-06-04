#!/usr/bin/python
# -*- coding: utf-8 -*-
# charger un fichier 'template' midi.
import sys
import os
import commands
import random
import csv
import copy

class MidiTemplate(object):
	def strip_notes_markers(self):
		for line in self.contents:
			if line.find("Note_on_c") != -1:
				print line

	def __init__(self, filename):
		print './mcsv/midicsv ' + filename
		output = commands.getstatusoutput('./mcsv/midicsv ' + filename)[1]
		lines = output.splitlines() 

		self.contents = []
		for line in lines:
			nl = line.split(',')
			# transforme les deux premières données
			# pour pouvoir faire des calculs dessus.
			nl[0] = int(nl[0])
			nl[1] = int(nl[1])

			# pareil pour les champs numériques des évenements
			# noteOn et noteOff
			if nl[2] == "Note_on_c" or nl[2] == "Note_off_c":
				nl[4] = int(nl[4])
				nl[5] = int(nl[5])

			self.contents.append(nl)

	def output_midi(self, outfile):
		outpipe = os.popen("./mcsv/csvmidi - " + outfile, "w")
		writer = csv.writer(outpipe)
		writer.writerows(self.contents)

	def set_starting_time(self,start_time):
		# start_time: le temps avec lequel
		# décaler la séquence
		for el in self.contents:
			el[1] += start_time
	
	def rewrite_notes(self, scale, attack):
		# Réecrit les notes en choisissant des notes de la gamme "scale"
		# au hasard, et des valeurs de velocité dans l'intervalle attack.
		for entry in self.contents:
			if entry[2] == " Note_on_c":
				oldvalue = entry[4]
				entry[4] = random.choice(scale)
				# Maintenant, trouve l'évenement Note_off_c correspondant :
				noteoff_entry = filter(lambda entry: entry[2] == " Note_off_c" and entry[4] == oldvalue,
				self.contents)[0]
				noteoff_entry[4] = entry[4]

				# Maintenant change la velocité :
				entry[5] = random.choice(attack)
	def __add__(self,y):

		def cond(el):
			if " Header" in el:
				return True
			if " Start_track" in el:
				return True
			if " Title_t" in el:
				return True
			if " Tempo" in el:
				return True
			if " Time_signature" in el:
				return True
			if " End_track" in el:
				return True
			if " End_of_file" in el:
				return True

			return False

		# enleve les élements de y qui empechent
		# d'additionner les deux séquences midi
		
		ny = copy.deepcopy(y)

		last = self.contents.pop() # recupère le truc End_of_file
		alast = self.contents.pop() # recupère le truc End_track
		ny.set_starting_time(alast[1])
		for el in ny.contents:
			if not cond(el):
				self.contents.append(el)

		alast[1] += self.contents[-1][1]
		last[1] = alast[1]
		self.contents += [alast]
		self.contents += [last]

		return self

if __name__ == "__main__":
	scale = [60, 61, 62, 63, 64, 65, 66, 67, 68]
	tmp = MidiTemplate(sys.argv[1])
	tmp.rewrite_notes(scale, scale)
	tmp2 = MidiTemplate(sys.argv[2])
	tmp2.rewrite_notes(scale, scale)
	tmp += tmp2
#	for e in tmp.contents:
#		print e
	tmp.output_midi('truc.mid')
