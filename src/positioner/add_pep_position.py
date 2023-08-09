# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import sys
import argparse
import logging
import pandas as pd
import numpy as np
from pyfaidx import Fasta

# from pysam import FastaFile
 
# fasta = "test.fasta"
# # read FASTA file
# sequences_object = FastaFile(fasta)


###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Include the peptide position within the protein in the report',
    epilog='''Examples:
        
    python  add_pep_position.py
      -i   test4/Npep2prot.tsv
      -f   test4/human_202206_pro-sw-tr.fasta
      -hp  peptide
      -hq  protein
      -o   test4/Npep2prot.new.tsv
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i',   required=True, help='Report file')
parser.add_argument('-f',   required=True, help='Protein sequences in FASTA format')
parser.add_argument('-hp',  required=True, help='Header name for the peptide level')
parser.add_argument('-hq',  required=True, help='Header name for the protein level')
parser.add_argument('-o',   required=True, help='Output file that is the Report file with the peptide positions')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


###################
# Local functions #
###################

# Union of multiple ranges from a list of tuples
# return a list of list (two elements: [start,end])
def union_ranges(a):
    b = []
    for begin,end in sorted(a):
        if b and b[-1][1] >= begin - 1:
            b[-1][1] = max(b[-1][1], end)
        else:
            b.append([begin, end])
    return b


#################
# Main function #
#################
def main(args):
    '''
    Main function
    '''    
    logging.info("getting the input parameters...")
    ifile1 = args.i
    ifile2 = args.f
    hp  = args.hp
    hq  = args.hq
    ofile = args.o



    logging.info("reading report file...")
    report = pd.read_csv(ifile1, sep="\t", header=[0,1], na_values=['NA', 'excluded'], low_memory=False) # two header rows



    logging.info("parsing the report file...")
    # Filter by levels
    rep = report[[(hp,'LEVEL'),(hq,'LEVEL')]]
    # rename the columns
    rep.columns = [c[0] for c in rep.columns]
    # Extract the raw peptide containing the delta-mass, if applicable.
    p = [i[0] for i in rep[hp].str.split('__')]
    rep[f"{hp}_raw"] = p
    # if the columns has ';' separator, then split the multiple proteins in a list an create one column.
    q = rep[hq].str.split(r"\s*;\s*", regex=True)
    rep[f"{hq}_raw"] = q



    logging.info("extracting the unique protein list...")
    proteins = np.unique(rep[f"{hq}_raw"].explode().values)
    proteins = np.unique(proteins)



    logging.info("reading fasta file filtering by the given proteins...")
    # get the protein id as key and filtering by the given list
    fasta_ite = Fasta(ifile2, key_function = lambda x: x.split('|')[1], filt_function = lambda x: x in proteins)
    # get the proteins from the fasta
    fasta_proteins = fasta_ite.keys()
    # get the protein seq from the fasta
    fasta_proteins_seq = dict([(q,fasta_ite[q][:].seq) for q in fasta_proteins])
    # get the protein seq from the fasta
    fasta_proteins_seqlen = dict([(q,len(s)) for q,s in fasta_proteins_seq.items()])
    
    

    logging.info("getting the sequences for the list of proteins...")
    # protein_seqs = [ [fasta_ite[q][:].seq for q in r if q in fasta_proteins] for r in rep[f"{hq}_raw"] ]
    # rep[f"{hq}_seqs"] = protein_seqs
    rep[f"{hq}_seqs"] = [ [fasta_proteins_seq[q] for q in r if q in fasta_proteins] for r in rep[f"{hq}_raw"] ]
    # add the length of sequences
    # protein_seqlen = [ [len(s) for s in r] for r in protein_seqs ]    
    # rep[f"{hq}_seqlen"] = protein_seqlen
    rep[f"{hq}_seqlen"] = [ [fasta_proteins_seqlen[q] for q in r if q in fasta_proteins] for r in rep[f"{hq}_raw"] ]
    
    
    
    logging.info("getting the sequence position for the protein list...")
    # get a list of tuple with the peptide and the list of proteins
    ps = list(zip(rep[f"{hp}_raw"],rep[f"{hq}_seqs"]))
    # add the start/end index of peptide
    peptide_pos = [ [ (s.find(r[0])+1,s.find(r[0])+len(r[0])) for s in r[1]] for r in ps ]
    rep[f"{hp}_pos"] = peptide_pos
    
    
    
    logging.info("getting the protein coverage...")
    # get a list of tuple with the protein and peptide positions
    qp = list(zip(rep[f"{hq}_raw"],rep[f"{hp}_pos"]))
    # merge the proteins with their peptide positions (merge two list into list of tuples)
    qpp = [list(zip(x,y)) for (x, y) in qp]
    # create protein dictionary (merge list of tuples based on the first element (protein_id))
    protein_pep_pos = {}
    for rr in qpp:
        for q,pp in rr:
            if q in protein_pep_pos:
                protein_pep_pos[q].append(pp)
            else:
                protein_pep_pos[q] = [pp]
    # get the union of ranges
    protein_pep_pos = dict([(q,union_ranges(pp)) for q,pp in protein_pep_pos.items()])    
    # count the number of aa per peptide range
    protein_pep_count = dict([(q,sum([p[1]-p[0]+1 for p in pp])) for q,pp in protein_pep_pos.items()])
    # for each protein in the report, add the coverage
    protein_coverage = [ [round(protein_pep_count[q]/fasta_proteins_seqlen[q],2) for q in r if q in protein_pep_count and q in fasta_proteins_seqlen] for r in rep[f"{hq}_raw"] ]
    rep[f"{hq}_coverage"] = protein_coverage
        
    

    logging.info("adding the result columns into report...")
    # join the int tuples into string (remembering that the int tuple is converting to str tuple)
    report[('peptide_pos','STATS')] = [';'.join(['-'.join(map(str,i)) for i in p]) for p in rep[f"{hp}_pos"]]
    # add the length of protein sequences
    report[('protein_seqlen','STATS')] = [';'.join(map(str,p)) for p in rep[f"{hq}_seqlen"]]
    # add the protein coverage
    report[('protein_coverage','STATS')] = [';'.join(map(str,p)) for p in rep[f"{hq}_coverage"]]
    


    logging.info("printing the output file...")
    report.to_csv(ofile, sep="\t", index=False)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

