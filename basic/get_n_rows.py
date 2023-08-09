# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import sys
import argparse
import logging
import pandas as pd

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Retrieve the N rows from the given file',
    epilog='''Examples:
        
    python  get_n_rows.py
      -i scan2pdm_outStats.tsv
      -n 10
      -o scan2pdm_outStats.n_rows.tsv      
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i',  required=True, help='Input table in tabular-separated format')
parser.add_argument('-n',  required=True, help='The number of rows')
parser.add_argument('-o',  required=True, help='Result containing N rows from the given table')

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
    n_rows = int(args.n)
    ofile = args.o

    logging.info("reading input file...")
    data = pd.read_csv(ifile, sep="\t", nrows=n_rows, low_memory=False)

    logging.info("printing the output file...")
    data.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

