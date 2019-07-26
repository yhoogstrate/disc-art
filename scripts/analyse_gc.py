#!/usr/bin/env python

import operator

gc = 0
at = 0


def gcat(ss):
	gc = 0
	at = 0

	for c in ss.upper():
		if c in 'GC':
			gc += 1
		elif c in 'AT':
			at += 1
		else:
			raise Exception("==> ERR: " + ss + " ["+c+"]")

	return( (gc, at) )


with open("/data/disc-o-art/tmp/SRR934949.Aligned.disc-art.txt", "r") as fh:
	for line in fh:
		k = line.strip().split("\t")[1]

		k = k.split("/")
		if k[0] != "AAAAAA" and k[0] != "TTTTTT":
			gc_at = gcat(k[0])

			gc += gc_at[0]
			at += gc_at[1]

		#print(k[0],"  ",gc_at, "    ",gc, " - ",at)

print(str(gc) + "/"+ str(at) + "=" + str(round(float(gc) / (float(gc) + float(at)),2)) )
