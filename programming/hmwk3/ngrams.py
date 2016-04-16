#!/usr/bin/env python

"""
Program to calculate the number of ngrams in the binary.
"""

__author__ = "Shivam Choudhary"
__uni__    = "sc3973"
import argparse
import os
import pprint
import binascii
import operator


class Ngrams(object):

    def __init__(self,n,s,in_file,out_file):
        """Initializing input parameters
            n:
                length of the ngrams.
            s:  
                length of the slide.
            in_file:
                input file name
            out_file:
                output file name 
        """
        self.n          = n
        self.s          = s
        self.in_file    = in_file
        self.out_file   = out_file
        self.calcNgrams()
    
    def calcNgrams(self):
        """ Calculates the Ngrams based on the input given.
        """
        ngrams = {} # A hash table to store the calculated ngrams
        f = open(self.in_file) # Returns the file descriptor for the in_file.
        offset =0 #Maintain the state of the slide.
        size = os.stat(self.in_file).st_size # Calculates the size of in_file
        while True:
            f.seek(offset) # Seek the file to current offset.
            chunk = f.read(self.n) # Read n bytes from the current seek position.
            offset+=self.s # update the offset with the slide.
            if len(chunk) <self.n: # Stop when read returns less than n.
                break
            else:
                key = binascii.hexlify(chunk) # hex of chunk used as a key
                try:
                    ngrams[key]+=1 # If entry exists in the ngrams hash table.
                except KeyError:
                    ngrams[key] = 1 # New key create entry for the key.
        sorted_ngram = sorted(ngrams.items(),key=operator.itemgetter(1),
                reverse=True) # Sort the hash table with the vales 
        pprint.pprint(sorted_ngram)

def main():
    """ Some Notation
        a) n is the length of the ngrams <int>
        b) s is the length of the slide <int> 
        c) in_file = name of the input file to analyse <string>
        d) out_file = output file name <string>
    """
    parser = argparse.ArgumentParser(description = "I am NGrams counter")
    parser.add_argument("n",type=int,help="an integer n that is the length"
            "of the ngrams")
    parser.add_argument("s",type=int, help="an integer s that is the length"
            " of the slide")
    parser.add_argument("in_file",type=str ,help="the name of the file to analyze")
    parser.add_argument("out_file",type=str, help="the name of the output file")
    args = parser.parse_args()

    ngrams = Ngrams(args.n, args.s, args.in_file, args.out_file)

if __name__=="__main__":
    main()



