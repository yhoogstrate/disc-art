#!/usr/bin/env python
# *- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 textwidth=79:


from discart.utils import sam_to_sorted_bam
from discart.detection import *

import unittest

from utils import main


class TestCases(unittest.TestCase):
    def test_001(self):
        test = "001"
        
        bam = sam_to_sorted_bam("tests/test_" + test + ".sam", "tmp/test_" + test + ".sorted.bam", "tmp")
        fa = "~/bio/fasta/hg38.fa"
        
        r = get_artifacted_reads(bam, fa)

        self.assertEqual(r, {})

 
if __name__ == '__main__':
    main()
