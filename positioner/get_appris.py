# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import sys
import os
import argparse
import logging
import re
import pandas as pd
import numpy as np
import subprocess
import concurrent.futures
from itertools import repeat



###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Retrieve APPRIS annotations for the given protein and positions',
    epilog='''Examples:
        
    python  get_appris.py
      -w   10
      -i   tests/test7/Paths_PDMTableMaker_PDMTable_GM_2.txt
      -c   q,b,e
      -d   Databases/APPRIS/202501/human/human_202501.appris.tsv
      -o   tests/test7/appris_annots.tsv
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-w',   type=int, default=4, help='Number of threads/n_workers (default: %(default)s)')
parser.add_argument('-i',   required=True, help='Table that contains protein and positions')
parser.add_argument('-c',   required=True, help='List of columns separated by commas that contain the protein ID, as well as the start position and end position')
parser.add_argument('-d',   required=True, help='APPRIS database in GTF format. By default, it is the local human database')
parser.add_argument('-o',   required=True, help='Output file that is the Report file with the peptide positions')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


#############
# Constants #
#############



###################
# Local functions #
###################
def split_str(x,a):
    try:
        # replace
        a = a.replace('_','-')
        # convert the lists into NumPy arrays
        X = x.split(";") if ';' in x else [x]
        A = a.split(";") if ';' in a else [a]
        # Combine the arrays element-wise
        C = [ x+':'+c for x in X for c in A ]
        return C
    except:
        return []

def split_2strs(x,a,b):
    try:
        # create query_index
        I = x+':'+a+'-'+b
        # convert the lists into NumPy arrays
        X = x.split(";") if ';' in x else [x]
        A = a.split(";") if ';' in a else [a]
        B = b.split(";") if ';' in b else [b]
        # Combine the arrays element-wise to obtain the Query
        Q = [ (I,cx+':'+c[0]+'-'+c[1]) for cx in X for c in zip(A,B) ]
        return Q
        # Q = [ (I,c) for c in Q ]
        # Q = [ cx+':'+c[0]+'-'+c[1] for cx in X for c in zip(A,B) ]
        # return [(I,Q)]
    except:
        return []
    
def run_tabix(q, bgzip, header):
    # get inputs from the query
    I = q[0]
    Q = q[1]
    # execute command
    proc = subprocess.Popen([f"tabix {bgzip} '{Q}'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True)
    (out, err) = proc.communicate()
    proc.stdout.close()  # close explicitly
    proc.stderr.close()
    proc.wait()  # ensure cleanup
    # convert bytes to strin
    out_str = out.decode('utf-8')
    # pre-processing the data
    out_dat = [ o.split('\t') for o in out_str.split('\n') if o != '']
    # create df
    df = pd.DataFrame(out_dat, columns=header)
    # insert the query in the first column
    df.insert(loc=0, column='query', value=I)
    return df



#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    n_workers = args.w
    q_ifile = args.i
    db_ifile = args.d
    q_cols  = re.split(r'\s*,\s*', args.c.strip())
    ofile = args.o
    

    # checking the appris database file
    if not os.path.exists(db_ifile):
        sys.exit("The APPRIS database file does not exist")
    
    
    logging.info("getting the header of appris database file...")
    db_header = pd.read_csv(db_ifile, sep="\t", nrows=0).columns.tolist()


    # creating a bgzip if applied...
    dbfile_bgzip = f"{db_ifile}.gz"
    if os.path.exists(dbfile_bgzip):
        logging.info("caching a bgzip file")
    else:
        logging.info("sorting and creating a bgzip...")
        os.system(f"(grep '^#' '{db_ifile}'; grep -v '^#' '{db_ifile}' | sort -t\"`printf '\t'`\" -k1,1 -k4,4n) | bgzip > '{dbfile_bgzip}'")
    # creating a tbi if applied...
    dbfile_tbi = f"{dbfile_bgzip}.tbi"
    if os.path.exists(dbfile_tbi):
        logging.info("caching a tabix file")
    else:
        logging.info("creating a tabix...")
        os.system(f"tabix -p gff '{dbfile_bgzip}'")




    logging.info(f"reading protein table using the {q_cols} columns...")
    q_rep = pd.read_csv(q_ifile, sep="\t", usecols=q_cols, low_memory=False)
    
    
    
    
    logging.info("pre-processing the queries...")
    # zip the columns depending the N cols
    # if there are multiple queries (start and end positions joined by ;) in one query, we split the query
    # q_cols = ['q','b','e']
    if len(q_cols) == 3:
        q_query = list(zip(q_rep.iloc[:,0], q_rep.iloc[:,1], q_rep.iloc[:,2]))
        q_query = [ qq for q in q_query if not pd.isna(q[0]) for qq in split_2strs(str(q[0]),str(q[1]),str(q[2])) ]
    # q_cols = ['q','f']
    elif len(q_cols) == 2:
        q_query = list(zip(q_rep.iloc[:,0], q_rep.iloc[:,1]))
        q_query = [ qq for q in q_query if not pd.isna(q[0]) for qq in split_str(str(q[0]),str(q[1])) ]
    # q_cols = ['q']
    else:
        q_query = list(zip(q_rep.iloc[:,0]))
    # unique queries
    q_query = list(set(q_query))




    logging.info("querying the protein:start-end in the appris annotations database...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:         
        q_results = executor.map( run_tabix, q_query, repeat(dbfile_bgzip), repeat(db_header))
    q_result = pd.concat(q_results)
    # drop duplicates
    q_result = q_result.drop_duplicates()




    logging.info("printing the output file...")
    q_result.to_csv(ofile, sep="\t", index=False)
    


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

