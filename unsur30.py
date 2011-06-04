#!/usr/bin/env python
# -*- coding: utf-8 -*-
# un sur 30 : ne conserve qu'une seule ligne toute les trente d'un fichier

import sys

def process_file(fname, count):
	i = 0
	fd = open(fname)
	lines = fd.readlines()
	ret = []

	for line in lines:
		if i % count == 0:
			i = 1
			ret.append(line)
			continue
		i += 1
	return ret

def output_result(res):
	for line in res:
		sys.stdout.write(line)

if __name__ == "__main__":
	ret = process_file(sys.argv[1], 30)
	output_result(ret)
