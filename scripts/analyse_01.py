#!/usr/bin/env python

import operator

rc = 0
identical = 0

keymap = {}



with open("/data/disc-o-art/tmp/SRR934949.Aligned.disc-art.txt", "r") as fh:
	for line in fh:
		k = line.strip().split("\t")[1]

		k = k.split("/")
		if k[0] == k[1]:
			identical += 1
			
			if not k[0] in keymap:
				keymap[k[0]] = 0
			keymap[k[0]] += 1
		else:
			rc += 1

			if not k[0] in keymap:
				keymap[k[0]] = 0
			keymap[k[0]] += 1

			if not k[1] in keymap:
				keymap[k[1]] = 0
			keymap[k[1]] += 1


# ratio identical ~= 1/6
#print (rc, '/' , identical)

sorted_x = sorted(keymap.items(), key=operator.itemgetter(1), reverse=True)

for _ in sorted_x:
	print(_[0] + "\t" + str(_[1]))
