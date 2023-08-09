# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import os
import sys
import argparse
import logging
import pandas as pd

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Convert BED file to FASTA',
    epilog='''Examples:
        
    python  convert_bed_to_fasta.py
      -i  tests/Ribo-seq_ORFs.bed
      -o  tests/Ribo-seq_ORFs.fasta
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i',  required=True, help='Bed file')
parser.add_argument('-o',  required=True, help='Output file in FASTA format that captures BED information')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#############
# Constants #
#############

BED_HEADERS = {
    0:  'chrom',
    1:  'chromStart',
    2:  'chromEnd',
    3:  'name',
    4:  'score',
    5:  'strand',
    6:  'thickStart',
    7:  'thickEnd',
    8:  'itemRgb',
    9:  'blockCount',
    10: 'blockSizes',
    11: 'blockStarts',
    12: 'labelId',
    13: 'none1',
    14: 'none2',
    15: 'none3',
    16: 'orfType',
    17: 'ensemblGeneId',
    18: 'geneName',
    19: 'geneType',
    20: 'transcriptType',
    21: 'peptideSeq',
    22: 'ensemblTranscriptIds',
    23: 'redundantGenes',
    24: 'none4',
    25: 'publications'
    }

META_HEADERS = [
    'labelId',
    'orfType',
    'ensemblGeneId',
    'geneName',
    'geneType',
    'transcriptType',
    'ensemblTranscriptIds',
    'redundantGenes',
    'publications'
    ]

#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    ifile = args.i
    ofile1 = args.o
    ofile2 = os.path.splitext(args.o)[0]+'.tsv'

    logging.info("reading input files...")
    data = pd.read_csv(ifile, sep="\t", header=None)
    
    logging.info("renaming the headers...")
    data.rename(columns=BED_HEADERS, inplace=True)
    
    logging.info("extracting the sequence ids...")
    ids = data['chrom'].astype(str)+':'+data['chromStart'].astype(str)+'-'+data['chromEnd'].astype(str)

    logging.info("extracting the sequences...")
    seqs = data['peptideSeq'].astype(str)

    logging.info("extracting the meta-data...")
    metas = data[META_HEADERS].values.tolist()

    logging.info("creating the fasta content...")
    ids_seqs = [z for z in zip(ids,seqs)]
    out_fasta = '\n'.join(['>'+t[0]+'\n'+t[1] for t in ids_seqs])

    logging.info("creating the meta-data content...")
    ids_metas = [z for z in zip(ids,metas)]
    out_meta = '\t'.join(['orfId']+META_HEADERS)+'\n'
    out_meta += '\n'.join([ '\t'.join([t[0]]+t[1]) for t in ids_metas])

    logging.info("printing the output files...")
    with open(ofile1, "w") as f:
        f.write(out_fasta)
    with open(ofile2, "w") as f:
        f.write(out_meta)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

