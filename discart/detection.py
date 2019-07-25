#!/usr/bin/env python

#import click
#from tqdm import tqdm


#import pysam
from pyfaidx import Fasta

#import discart
#from utils import *



def get_artifacted_reads(input_fasta_file, input_alignment_file):

    # index to search for string codes
    query_idx = {}
    artifacted = []

    with Fasta(input_fasta_file) as genes, pysam.AlignmentFile(input_alignment_file, "rb") as fh:
        for _ in fh.fetch():
            if _.has_tag('SA'):
                for __ in [__ for __ in _.get_tag('SA').split(";") if len(__) > 0]:
                    __ = __.split(",")
                    __[1] = int(__[1]) 
                    #print(_.query_name + " :  " , __)

                    a = str(genes[__[0]][__[1] - 6 - 1:__[1] - 1]).upper()
                    b = str(genes[__[0]][__[1] - 1 : __[1] - 1 + 6]).upper()

                    end = __[1] + bam_parse_alignment_offset(cigar_to_cigartuple(__[3]))
                    c = str(genes[__[0]][end - 6 - 1: end - 1]).upper()
                    d = str(genes[__[0]][end - 1: end - 1 + 6]).upper()

                    if not _.query_name in query_idx:
                        query_idx[_.query_name] = set([a, b, c, d])
                    else:
                        isct = query_idx[_.query_name].intersection(set([a, b, c, d]))
                        isct = [_+"/"+_ for _ in isct]

                        if len(  isct  ) == 1:
                            artifacted.append([_.query_name, list(isct)])
                        else:
                            isct = query_idx[_.query_name].intersection(set([revcomp(a), revcomp(b), revcomp(c), revcomp(d)]))
                            isct = [_+"/"+revcomp(_) for _ in isct]

                            if len(  isct  ) == 1:
                                artifacted.append([_.query_name, list(isct)])

                        # assume only 2 split reads per mate - if the second is encountered, idx can safely be cleaned
                        del(query_idx[_.query_name])

    return artifacted


