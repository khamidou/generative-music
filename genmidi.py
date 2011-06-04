# -*- coding: utf-8 -*-
from miditrack import MidiTemplate
from random import choice as random_choice

def generate_drum_track(l, outfile):
	# génere les données depuis une piste de batterie
	b_bien = ["boucles/1.mid", "boucles/2.mid", "boucles/3.mid"]
	b_moyen = ["boucles/5.mid", "boucles/6.mid", "boucles/7.mid"]
	b_pasbien = ["boucles/8.mid", "boucles/9.mid", "boucles/10.mid"]
	b_mauvais = ["boucles/11.mid", "boucles/12.mid", "boucles/13.mid"]

	d = l[0][1]
	
	if d["pente"] == "elevé":
		ret = MidiTemplate(random_choice(b_bien))
	elif d["pente"] == "moyen":
		ret = MidiTemplate(random_choice(b_moyen))
	elif d["pente"] == "faible":
		ret = MidiTemplate(random_choice(b_mauvais))
		# FIXME : quatre types de boucles, et juste trois caractéristiques.

	for e in l[1:10]: #FIXME: changer l'intervalle
		d = e[1]

		if d["pente"] == "elevé":
			tmp = MidiTemplate(random_choice(b_bien))
		elif d["pente"] == "moyen":
			tmp = MidiTemplate(random_choice(b_moyen))
		elif d["pente"] == "faible":
			tmp = MidiTemplate(random_choice(b_mauvais))

		ret += tmp
	
	ret.output_midi(outfile)

def rewrite_notes(midi_template, moyenne="elevé", ecart_type="elevé", pente="elevé") 
	if moyenne == "elevé":
		# réglage du volume sonore.
		fvolume = lambda: return random.choice(range(90, 127))
	elif moyenne == "moyenne":
		fvolume = lambda: return random.choice(range(45, 90))
	elif moyenne == "faible":
		fvolume = lambda: return random.choice(range(1, 45))

	if ecart_type == "elevé":
		# sélection de la gamme
		fgamme = lambda: return random.choice(range(90, 127))
	elif ecart_type == "ecart_type":
		fgamme = lambda: return random.choice(range(45, 90))
	elif ecart_type == "faible":
		fgamme = lambda: return random.choice(range(1, 45))

def generate_piano_track(l, outfile):
	
