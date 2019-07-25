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
        
        r = get_artifacted_reads(fa, bam)
        self.assertEqual(r, [['SRR934949.17215595', ['ATGTGG/CCACAT']]])
        
        r = get_artifacted_read_numbers(fa, bam)
        self.assertEqual(r, (1, 0))

 
if __name__ == '__main__':
    main()
