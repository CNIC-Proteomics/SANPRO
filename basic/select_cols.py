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
import numpy as np


###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Remove the specified columns from the table',
    epilog='''Examples:
        
    python  remove_cols.py
      -i  scan2pdm_outStats.tsv
      -c  idinf,Xinf,Vinf
      -o  scan2pdm_outStats.removed_cols.tsv
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i',  required=True, help='Input table in tabular-separated format')
parser.add_argument('-c',  help='Columns separated by commas that determine the differences between files')
parser.add_argument('-o',  required=True, help='Output file without the specified columns')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

###################
# Local functions #
###################

#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    ifile = args.i
    cols = re.split('\s*,\s*',args.c) if args.c and args.c != '' else []
    ofile = args.o

    logging.info("reading input files...")
    data = pd.read_csv(ifile, sep="\t", low_memory=False)

    logging.info(f"checking the given columns: {cols}")
    # get the columns that do not exist in the table
    cc = [c for c in cols if not c in data.columns]
    if len(cc) > 0:
        sms = f"The specified columns do not exist in the provided table: {cc}"
        logging.error(sms)
        sys.exit(sms)

    logging.info("selecting the given columns...")
    data = data[cols]
    
    logging.info("removing duplicates...")
    data = data.drop_duplicates()
    
    logging.info("printing the output file...")
    data.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

