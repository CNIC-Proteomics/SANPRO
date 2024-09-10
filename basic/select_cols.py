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
    description='Select the specified columns from the table.',
    epilog='''Usages:
        
    python  select_cols.py  -c config.ini
    
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
    ifile = conf_args['infile']
    ofile = conf_args['outfile']
    nh = int(conf_args['n_headers']) if 'n_headers' in conf_args else 1
    cols = re.split('\s*;\s*', conf_args['cols']) if args.c and args.c != '' else []
    # if there are 2 headers, convert the lsit of tuples
    cols = [ eval(c) for c in cols ] if nh == 2 else cols

    logging.info(f"reading input files with {nh} headers...")
    if nh == 2:
        data = pd.read_csv(ifile, sep="\t", low_memory=False, header=[0,1]) # two headers
    else:
        data = pd.read_csv(ifile, sep="\t", low_memory=False, nrows=10)

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

