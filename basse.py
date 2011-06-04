#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

*** Description ***

	Converts a progression to chords and plays them using fluidsynth.

	You should specify the SF2 soundfont file.

"""

from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note, Track
from mingus.midi.MidiFileOut import write_Track
import time, sys
from random import random

def strip_chords(l):
	# une fonction pour ne garder que la fondamentale
	# d'un accord, sinon mingus nous le joue en arpeggié
	ret = []
	for e in l:
		ret.append(e[0])
	return ret

progression = ["I", "vi", "iv", "V7"]
key = 'C'

chords = progressions.to_chords(progression, key)
notes = strip_chords(chords)
tr = Track()
for note in notes:
	tr.add_notes(note, duration=1)

write_Track('out.mid', tr)
