# -*- coding: utf-8 -*-
"""
@author: jmrodriguezc
"""

# import global modules
import configparser

#########################
# Import local packages #
#########################

####################
# Global variables #
####################

####################
# Common functions #
####################
def read_config(name, cfile):
    config = configparser.ConfigParser()
    config.read(cfile)
    # remove " from values
    args = { k: v.strip('"') for k,v in config[name].items() }
    return args


if __name__ == "__main__":
	print("It is a library used by SANPRO programs")