# -*- coding: utf-8 -*-
from miditrack import MidiTemplate
from random import choice as random_choice

def generate_drum_track(l, outfile):
	# génere les données depuis une piste de batterie
	b_bien = ["boucles/1.mid", "boucles/2.mid", "boucles/3.mid"]
	b_moyen = ["boucles/5.mid", "boucles/6.mid", "boucles/7.mid"]
	b_pasbien = ["boucles/8.mid", "boucles/9.mid", "boucles/10.mid"]
	b_mauvais = ["boucles/11.mid", "boucles/12.mid", "boucles/13.mid"]

	# FIXME : quatre types de boucles, et juste trois caractéristiques.

	ret = None
	for e in l[1:10]: #FIXME: changer l'intervalle
		d = e[1]

		if d["pente"] == "elevé":
			tmp = MidiTemplate(random_choice(b_bien))
		elif d["pente"] == "moyen":
			tmp = MidiTemplate(random_choice(b_moyen))
		elif d["pente"] == "faible":
			tmp = MidiTemplate(random_choice(b_mauvais))

		if ret == None:
			ret = tmp
		else:		
			ret += tmp
	
	ret.output_midi(outfile)

def choose_rewrite_interval(midi_template, moyenne="elevé", ecart_type="elevé", pente="elevé"):
	# sélectionne les intervalles de réecriture selon les paramètres statistiques.
	if moyenne == "elevé":
		# réglage du volume sonore.
		volume = range(90, 127)
	elif moyenne == "moyenne":
		volume = range(45, 90)
	else:
		volume = range(1, 45) + range(100, 127)

	if ecart_type == "elevé": #FIXME: je crois que ça dépend de la pente...
		# sélection de la gamme
		gamme = [60, 62, 64, 65, 67, 69, 71] # gamme majeure FIXME: virer le triton  
	elif ecart_type == "ecart_type":
		gamme = [60, 62, 63, 65, 67, 68, 70] # gamme mineure
	else:
		gamme = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71] # gamme "dodécaphonique" - sérialisme intégral 
	
	midi_template.rewrite_notes(volume, gamme)

def generate_piano_track(l, outfile):
	b_bien = ["boucles/1.mid", "boucles/2.mid", "boucles/3.mid"]
	b_moyen = ["boucles/5.mid", "boucles/6.mid", "boucles/7.mid"]
	b_mauvais = ["boucles/11.mid", "boucles/12.mid", "boucles/13.mid"]

	d = l[0][1]
	
	ret = None	
	for e in l[1:10]: #FIXME: changer l'intervalle
		d = e[1]

		if d["pente"] == "elevé":
			tmp = MidiTemplate(random_choice(b_bien))
		elif d["pente"] == "moyen":
			tmp = MidiTemplate(random_choice(b_moyen))
		elif d["pente"] == "faible":
			tmp = MidiTemplate(random_choice(b_mauvais))

		choose_rewrite_interval(tmp, d["moyenne"], d["ecart"], d["pente"])

		if ret == None:
			ret = tmp
		else:
			ret += tmp
	
	ret.output_midi(outfile)

