# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import sys
import argparse
import logging
import re
import pandas as pd

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Retrieve the rows that differ based on specified columns from two tabular-separated files',
    epilog='''Examples:
        
    python  diff_files.py
      -i1 scan2pdm_tagged.tsv
      -i2 scan2pdm_tagged2.tsv
      -c  idsup,idinf,tags
      -o  output.tsv
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i1',  required=True, help='First file')
parser.add_argument('-i2',  required=True, help='Second file')
parser.add_argument('-c',  help='Columns separated by commas that determine the differences between files')
parser.add_argument('-o',  required=True, help='Output file that captures the differences between the files')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    ifile1 = args.i1
    ifile2 = args.i2
    cols = re.split('\s*,\s*',args.c) if args.c and args.c != '' else []
    ofile = args.o

    logging.info("reading input files...")
    data1 = pd.read_csv(ifile1, sep="\t", low_memory=False)
    data2 = pd.read_csv(ifile2, sep="\t", low_memory=False)

    logging.info("generating a prefix in the index for file identification purposes...")
    data1.rename('{}_1'.format, inplace=True)
    data2.rename('{}_2'.format, inplace=True)

    if len(cols) > 0:
        logging.info(f"getting the differences based on the given columns: {cols} ...")
        # take into account the given columns
        diff = pd.concat([data1,data2]).drop_duplicates(subset=cols, keep=False)
    else:
        logging.info("getting the differences based on all columns...")
        # take into account all columns
        diff = pd.concat([data1,data2]).drop_duplicates(keep=False)

    logging.info("adding a column for file identification purposes...")
    diff['file_label'] = [ 'file1' if i.endswith('_1') else 'file2' for i in diff.index]

    logging.info("printing the output file...")
    diff.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

