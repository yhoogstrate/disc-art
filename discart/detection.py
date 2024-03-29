#!/usr/bin/env python


import pysam
from pyfaidx import Fasta

import discart
from .utils import *



def get_read_uid(read):
    if read.is_paired: # it is theoretically possible that both mates are split. in that case unique id's are needed:
        if read.is_read1:
            uid = '1' + read.query_name
        else:
            uid = '2' + read.query_name
    else:
        uid = '0' + read.query_name

    return uid



def get_hexamers(genes, splitread, kmer_size):
    """
    By CIGAR string
    """

    if splitread.has_tag('SA'):
        sa_tags = [_ for _ in splitread.get_tag('SA').split(";") if _.strip() != '']
        if len(sa_tags) >= 1:
            try:
                a = str(genes[splitread.reference_name][splitread.reference_start - kmer_size:splitread.reference_start]).upper()
                b = str(genes[splitread.reference_name][splitread.reference_start: splitread.reference_start + kmer_size]).upper()

                c = str(genes[splitread.reference_name][splitread.reference_end - kmer_size: splitread.reference_end]).upper()
                d = str(genes[splitread.reference_name][splitread.reference_end: splitread.reference_end + kmer_size]).upper()
            except:
                return None

            return([a, b, c, d])

    return None

def get_hexamers_from_other_splitread(genes, splitread, kmer_size):
    """
    Do not use CIGAR string but SA: tag of other piece of the read
    """

    if splitread.has_tag('SA'):
        sa_tags = [_ for _ in splitread.get_tag('SA').split(";") if _.strip() != '']
        if len(sa_tags) > 1:
            raise Exception("Not sure when this happens, if this happens")
        elif len(sa_tags) == 1:
            sa_tag = sa_tags[0].split(",")
            sa_tag[1] = int(sa_tag[1]) 

            a = str(genes[sa_tag[0]][sa_tag[1] - kmer_size - 1:sa_tag[1] - 1]).upper()
            b = str(genes[sa_tag[0]][sa_tag[1] - 1 : sa_tag[1] - 1 + kmer_size]).upper()

            end = sa_tag[1] + bam_parse_alignment_offset(cigar_to_cigartuple(sa_tag[3]))
            c = str(genes[sa_tag[0]][end - kmer_size - 1: end - 1]).upper()
            d = str(genes[sa_tag[0]][end - 1: end - 1 + kmer_size]).upper()
            
            return([a, b, c, d])

    return None



def get_artifacted_reads(input_fasta_file, input_alignment_file, by_sa, kmer_size):

    # index to search for string codes
    query_idx = {}
    artifacted = []

    with Fasta(str(input_fasta_file)) as genes, pysam.AlignmentFile(input_alignment_file, "rb") as fh:
        for _ in fh.fetch():
            uid = get_read_uid(_) # it is theoretically possible that both mates are split. in that case unique id's are needed

            if by_sa:
                sequences = get_hexamers_from_other_splitread(genes, _, kmer_size)
            else:
                sequences = get_hexamers(genes, _, kmer_size)

            if sequences:
                if not uid in query_idx:
                    query_idx[uid] = set(sequences)
                else:
                    isct = query_idx[uid].intersection(set(sequences))
                    isct = [_ + "/" + _ for _ in isct]

                    if len(  isct  ) == 1:
                        artifacted.append([uid, list(isct)])
                    else:
                        sequences_rc = set([revcomp(sequences[0]), revcomp(sequences[1]), revcomp(sequences[2]), revcomp(sequences[3])])

                        isct = query_idx[uid].intersection(sequences_rc)
                        isct = [_ + "/" + revcomp(_) for _ in isct]

                        if len(  isct  ) == 1:
                            artifacted.append([uid[1:], list(isct)])

                    # assume only 2 split reads per mate - if the second is encountered, idx can safely be cleaned
                    del(query_idx[uid])

    return artifacted



def get_artifacted_read_numbers(input_fasta_file, input_alignment_file, by_sa, kmer_size):
    query_idx = {}# index to search for string codes

    artifacted = set([])
    all_ids = set([]) # concordant reads

    with Fasta(str(input_fasta_file)) as genes, pysam.AlignmentFile(input_alignment_file, "rb") as fh:
        for _ in fh.fetch():
            all_ids.add(_.query_name)
            uid = get_read_uid(_) # it is theoretically possible that both mates are split. in that case unique id's are needed

            if by_sa:
                sequences = get_hexamers_from_other_splitread(genes, _, kmer_size)
            else:
                sequences = get_hexamers(genes, _, kmer_size)

            if sequences:
                if not uid in query_idx:
                    query_idx[uid] = set(sequences)
                else:
                    isct = query_idx[uid].intersection(set(sequences))
                    isct = [_+"/"+_ for _ in isct]

                    if len(  isct  ) == 1:
                        artifacted.add(uid[1:])
                    else:
                        sequences_rc = set([revcomp(sequences[0]), revcomp(sequences[1]), revcomp(sequences[2]), revcomp(sequences[3])])

                        isct = query_idx[uid].intersection(sequences_rc)
                        isct = [_+"/"+revcomp(_) for _ in isct]

                        if len(  isct  ) == 1:
                            artifacted.add(uid[1:])

    n = len(artifacted) # number artifacted
    return (n, len(all_ids) - n)


