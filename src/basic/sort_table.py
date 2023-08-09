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
    description='Sort the table file (in tabular-separated format) based on the specified columns',
    epilog='''Examples:
        
    python  sort_table.py
      -i scan2pdm_outStats.tsv
      -s  idsup,Z,tags
      -o  scan2pdm_outStats.sorted.tsv
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i',  required=True, help='Input table in tabular-separated format')
parser.add_argument('-s',  required=True, help='Columns separated by commas that sort the result file')
parser.add_argument('-o',  required=True, help='Sorted input file')
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
    ifile = args.i
    cols_order = re.split('\s*,\s*',args.s) if args.s and args.s != '' else []
    ofile = args.o

    logging.info("reading input file...")
    data = pd.read_csv(ifile, sep="\t", low_memory=False)

    logging.info(f"sorting by the given columns: {cols_order}...")
    data.sort_values(cols_order, ascending=True, inplace=True)

    logging.info("printing the output file...")
    data.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

