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
import plotly.express as px
import plotly.graph_objects as go
# import plotly.io as pio
# pio.renderers.default = 'png'
# pio.renderers.default = 'browser'


###################
# Parse arguments #
###################

parser = argparse.ArgumentParser(
    description='Create a scatter plot using the column values from two tables (tabular-separated files)',
    epilog='''Examples:
        
    python  cmp_val_tables.py
      -i1 test3/scan2pdm_outStats.1.tsv
      -i2 test3/scan2pdm_outStats.2.tsv
      -id1  idsup,idinf
      -id2  idsup,idinf
      -c1   Z
      -c2   Z
      -o  test3/scatterplot_1_vs_2.png
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i1',  required=True, help='First file')
parser.add_argument('-i2',  required=True, help='Second file')
parser.add_argument('-id1', required=True, help='Columns separated by commas that identify the row in first table')
parser.add_argument('-id2', required=True, help='Columns separated by commas that identify the row in second table')
parser.add_argument('-c1',  required=True, help='Column that selects the values to compare in the first table')
parser.add_argument('-c2',  required=True, help='Column that selects the values to compare in the second table')
parser.add_argument('-o',   required=True, help='Output file where the scatter plot image is saved')
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
    id1 = re.split('\s*,\s*',args.id1) if args.id1 and args.id1 != '' else []
    id2 = re.split('\s*,\s*',args.id2) if args.id2 and args.id2 != '' else []
    c1  = args.c1
    c2  = args.c2
    ofile = args.o


    logging.info("reading input files...")
    import os
    idir = os.path.dirname(__file__)
    ifile1 = os.path.join(idir, ifile1)
    ifile2 = os.path.join(idir, ifile2)
    ofile = os.path.join(idir, ofile)

    data1 = pd.read_csv(ifile1, sep="\t", low_memory=False)
    data2 = pd.read_csv(ifile2, sep="\t", low_memory=False)
    
    
    logging.info("removing outliers if applicable...")
    if 'tags' in data1.columns:
        data1 = data1[data1['tags'].str.contains('out', na=False) == False]
    if 'tags' in data2.columns:
        data2 = data2[data2['tags'].str.contains('out', na=False) == False]


    logging.info("obtaining the specified columns: [id's + c]...")
    data1 = data1[id1+[c1]]
    data2 = data2[id2+[c2]]
    
    
    logging.info("setting the id columns as row index...")
    data1 = data1.set_index(id1)
    data2 = data2.set_index(id2)
    

    logging.info("preparing the data for the plot...")
    s1 = '_1'
    s2 = '_2'
    data = pd.concat([data1.add_suffix(s1), data2.add_suffix(s2)], axis=1)


    logging.info("creating the plot...")
    lbl_x = f"{c1} Old sanxotsieve"
    lbl_y = f"{c2} New sanxotsieve byPercentage10"
    data_x = data[f"{c1}{s1}"]
    data_y = data[f"{c2}{s2}"]
    line_min = int( min(data_x.min(),data_y.min())-1 )
    line_max = int( max(data_x.max(),data_y.max())+1 )
    # convert the nan values to minimun value
    data_x = data_x.fillna(data_y.min())
    data_y = data_y.fillna(data_x.min())
    
    fig = px.scatter(x=data_x, y=data_y, labels={'x': lbl_x, 'y': lbl_y}, range_x=[line_min,line_max], range_y=[line_min,line_max])
    fig.add_trace(
        go.Scatter(
        x=[line_min,line_max],
        y=[line_min, line_max],
        mode="lines",
        line=go.scatter.Line(color="red"),
        showlegend=False)
    )
    # fig.show()


    logging.info("saving the plot in the output file...")
    # plt.savefig(ofile)
    # fig.write_html(ofile)
    fig.write_image(ofile)


if __name__ == "__main__":
    # start main function
    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end script')

