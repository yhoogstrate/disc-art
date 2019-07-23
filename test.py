#!/usr/bin/env python

import pysam
from pyfaidx import Fasta

bam = "/data/disc-o-art/tmp/test_001.Aligned.out.sorted.bam"
fa = "/home/youri/bio/fasta/hg38.fa"




#from string import maketrans

def revcomp(seq):
    return seq.translate(maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]
    
    


with Fasta(fa) as genes, pysam.AlignmentFile(bam, "rb") as fh:
        print("ALIVE")
        
        for _ in fh.fetch():
            if _.has_tag('SA'):
                for __ in [__ for __ in _.get_tag('SA').split(";") if len(__) > 0]:
                    __ = __.split(",")
                    __[1] = int(__[1])
                    print(_.query_name + " :  " , __)
                    print ("     A   : ",genes[__[0]][__[1] - 6:__[1]])
                    print ("     A,rc: ",revcomp(genes[__[0]][__[1] - 6:__[1]]))
