#!/usr/bin/env python
# *- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 textwidth=79:

import os
import unittest

from discart.utils import sam_to_sorted_bam
from discart.detection import *

from utils import main


class TestCases(unittest.TestCase):
    def test_001(self):
        test = "001"
        
        bam = sam_to_sorted_bam("tests/data/test_" + test + ".sam", "tmp/test_" + test + ".sorted.bam", "tmp")
        fa = os.path.expanduser("~/bio/fasta/hg38.fa")

        r = get_artifacted_reads(fa, bam, False)
        self.assertEqual(r, [['SRR934949.17215595', ['CCACAT/ATGTGG']]])

        r = get_artifacted_reads(fa, bam, True)
        self.assertEqual(r, [['SRR934949.17215595', ['ATGTGG/CCACAT']]])

        r1 = get_artifacted_read_numbers(fa, bam, True)
        r2 = get_artifacted_read_numbers(fa, bam, False)
        self.assertEqual(r1, (1, 0))
        self.assertEqual(r2, (1, 0))

    def test_002(self):
        test = "002"
        
        bam = sam_to_sorted_bam("tests/data/test_" + test + ".sam", "tmp/test_" + test + ".sorted.bam", "tmp")
        fa = os.path.expanduser("~/bio/fasta/hg38.fa")

        r = get_artifacted_reads(fa, bam, False)
        self.assertEqual(r, [['SRR934949.17215595', ['CCACAT/ATGTGG']]])

        r = get_artifacted_reads(fa, bam, True)
        self.assertEqual(r, [['SRR934949.17215595', ['ATGTGG/CCACAT']]])

        r1 = get_artifacted_read_numbers(fa, bam, True)
        r2 = get_artifacted_read_numbers(fa, bam, False)
        self.assertEqual(r1, (1, 2)) # 1 artifacted | 1 concordant + 1 non-artifacted split read
        self.assertEqual(r2, (1, 2)) # 1 artifacted | 1 concordant + 1 non-artifacted split read


    def test_003(self):
        test = "003"
        
        bam = sam_to_sorted_bam("tests/data/test_" + test + ".sam", "tmp/test_" + test + ".sorted.bam", "tmp")
        fa = os.path.expanduser("~/bio/fasta/hg38.fa")

        r = get_artifacted_reads(fa, bam, False)
        #self.assertEqual(r, [['SRR934949.17215595', ['CCACAT/ATGTGG']]])


 
if __name__ == '__main__':
    main()
