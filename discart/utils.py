#!/usr/bin/env python

import os
import pysam

def cigar_to_cigartuple(cigar_str):
    """Converts a CIGAR string into a tuple compatible with Pysam.
    E.g. '10M5S' becomes: [(0, 10), (4, 5)]
    """
    tt = {'M': 0,  # BAM_CMATCH	0
          'I': 1,  # BAM_CINS	1
          'D': 2,  # BAM_CDEL	2
          'N': 3,  # BAM_CREF_SKIP	3
          'S': 4,  # BAM_CSOFT_CLIP	4
          'H': 5,  # BAM_CHARD_CLIP	5
          'P': 6,  # BAM_CPAD	6
          '=': 7,  # BAM_CEQUAL	7
          'X': 8}  # BAM_CDIFF	8

    cigartup = []

    for chunk in pat_bam_parse_alignment_offset_using_cigar.finditer(cigar_str):
        flag = chunk.group(2)
        length = chunk.group(1)
        cigartup.append((tt[flag], int(length)))

    return cigartup


def sam_to_sorted_bam(sam, fixed_bam, T_TEST_DIR):
    basename, ext = os.path.splitext(os.path.basename(sam))
    bam_file = T_TEST_DIR + '/' + basename + '.bam'

    pysam.sort('-o', bam_file, sam)
    pysam.index(bam_file)

    return bam_file

def bam_diff(f1, f2, T_TEST_DIR):
    basename, ext = os.path.splitext(os.path.basename(f1))

    f1sorted = T_TEST_DIR + basename + '.f1.sorted.bam'
    f2sorted = T_TEST_DIR + basename + '.f2.sorted.bam'

    pysam.sort(f1, '-n', '-o', f1sorted)
    pysam.sort(f2, '-n', '-o', f2sorted)

    f1sam = T_TEST_DIR + basename + '.f1.sam'
    f2sam = T_TEST_DIR + basename + '.f2.sam'

    fhq = open(f1sam, "w")
    fhq.write(pysam.view('-h', f1sorted))
    fhq.close()

    fhq = open(f2sam, "w")
    fhq.write(pysam.view('-h', f2sorted))
    fhq.close()

    subprocess.Popen(['sed', '-i', '-r', 's@(SA:[^\\t]+)\\t(LB:[^\\t]+)\t(RG:[^\\t]+)@\\3\\t\\1\\t\\2@', f2sam], stdout=subprocess.PIPE).stdout.read()

    subprocess.Popen(['sed', '-i', '-r', 's@\\tFI:i:[0-9]+@@', f1sam], stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen(['sed', '-i', '-r', 's@\\tFI:i:[0-9]+@@', f2sam], stdout=subprocess.PIPE).stdout.read()

    # one time only
    # subprocess.Popen(['sed', '-i' , '-r', 's@\\tSA:Z:[^\\t]+@@', f1sam], stdout=subprocess.PIPE).stdout.read()
    # subprocess.Popen(['sed', '-i' , '-r', 's@\\tSA:Z:[^\\t]+@@', f2sam], stdout=subprocess.PIPE).stdout.read()

    return filecmp.cmp(f1sam, f2sam), f1sam, f2sam

def bam_parse_alignment_offset(cigartuple, skip_N=False):
    pos = 0

    if skip_N:
        charset = [0, 2,     7, 8]
    else:
        charset = [0, 2, 3,  7, 8]

    for chunk in cigartuple:
        """ M	BAM_CMATCH	0
            I	BAM_CINS	1
            D	BAM_CDEL	2
            N	BAM_CREF_SKIP	3
            S	BAM_CSOFT_CLIP	4
            H	BAM_CHARD_CLIP	5
            P	BAM_CPAD	6
            =	BAM_CEQUAL	7
            X	BAM_CDIFF	8
            """

        if chunk[0] in charset:
            pos += chunk[1]

    return pos


def revcomp(seq):
    return seq.translate(str.maketrans("ACTGactg","TGACtgac"))
    
