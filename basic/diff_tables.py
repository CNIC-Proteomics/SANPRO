# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import os
import sys
import argparse
import logging
import re
import pandas as pd

#########################
# Import local packages #
#########################
sys.path.append(f"{os.path.dirname(__file__)}/../libs")
import common

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Retrieve the rows that differ based on specified columns from two tabular-separated files.',
    epilog='''Usages:
        
    python  diff_tables.py  -c config.ini
    
    Note: Please read the config file to determine which parameters should be used.
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-c', required=True, help='Config input file in INI format')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# get the name of script
script_name = os.path.splitext( os.path.basename(__file__) )[0].upper()


#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    conf_args = common.read_config(script_name, args.c)
    [ print(f"{k} = {v}") for k,v in conf_args.items() ]
    ifile1 = conf_args['infile1']
    ifile2 = conf_args['infile2']
    cols = re.split('\s*,\s*', conf_args['cols']) if args.c and args.c != '' else []
    ofile = conf_args['outfile']
    
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

