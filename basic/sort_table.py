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
    description='Sort the table file (in tabular-separated format) based on the specified columns.',
    epilog='''Usages:
        
    python  sort_table.py  -c config.ini
    
    Note: Please read the config file to determine which parameters should be used.
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-c', required=True, help='Config input file in YAML format')
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
    ifile = conf_args['infile']
    cols = re.split('\s*,\s*', conf_args['cols']) if args.c and args.c != '' else []
    ofile = conf_args['outfile']

    logging.info("reading input file...")
    data = pd.read_csv(ifile, sep="\t", low_memory=False)

    logging.info(f"sorting by the given columns: {cols}...")
    data.sort_values(cols, ascending=True, inplace=True)

    logging.info("printing the output file...")
    data.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

