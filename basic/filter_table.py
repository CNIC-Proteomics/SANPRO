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
import numpy as np

#########################
# Import local packages #
#########################
sys.path.append(f"{os.path.dirname(__file__)}/../libs")
import common

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Filter the given table file based on the provided conditions (header, operator, value).',
    epilog='''Usages:
        
    python  filter_table.py  -c config.ini
    
    Note: Please read the config file to determine which parameters should be used.
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-c', required=True, help='Config input file in YAML format')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# get the name of script
script_name = os.path.splitext( os.path.basename(__file__) )[0].upper()

###################
# Local functions #
###################

def filter_dataframe(df, flt):
    '''
    Filter the dataframe

    Parameters
    ----------
    df : pandas dataframe
    flt : str (boolean expression)
        Example: ([FDR] < 0.05) & ([n] >= 10) & ([n] <= 100)
    Returns
    -------
    Filtered dataframe.

    '''
    # flag that controls whether the df was filtered or not.
    ok = False
    # check if the given filters is applied into given dataframe
    f_cols = re.findall(r'\[([^\]]*)\]',flt)
    intcols = np.intersect1d(df.columns,f_cols).tolist() if f_cols else []
    # the columns in the filters are within df
    if intcols:    
        # add the df variable
        flt = flt.replace("[","['").replace("]","']")
        flt = flt.replace('[','df[')
        flt = f"df[{flt}]"
        try:
            # evaluate condition
            idx = pd.eval(flt)
            # extract the dataframe from the index
            if not idx.empty:
                df_new = df.loc[idx.index.to_list(),:]
                df_new = df_new.reset_index()
                df_new.drop(columns=df_new.columns[0], axis=1, inplace=True)
                ok = True
            else:
                # not filter
                logging.warning("The filter has not been applied")
                df_new = df
        except Exception as exc:
            # not filter
            logging.warning(f"The filter has not been applied. There was a problem evaluating the condition: {flt}\n{exc}")
            df_new = df
    else:
        df_new = df

    return ok,df_new

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
    ifilter = conf_args['filter']
    # ifilter = "([tags] == 'out')"
    # ifilter = "([idsup] == 'AAFTECCQAAD\[160.01746\]K')" # This is not work due to the brackets in the sequence :-(
    ofile = conf_args['outfile']


    logging.info("reading input files...")
    data = pd.read_csv(ifile, sep="\t", low_memory=False)

    logging.info("filtering the input table...")
    ok_flt,data_f = filter_dataframe(data, ifilter)
    if not ok_flt:
        sms = "The filter has not been applied"
        logging.error(sms)
        sys.exit(sms)

    logging.info("printing the output file...")
    data_f.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

