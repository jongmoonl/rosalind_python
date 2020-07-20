#!/usr/bin/env python3
# Purpose: Construct the Overlap Graph of a Collection of k-mers

import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3c.
    '''

    def __init__ (self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname

    def doOpen (self):
        if self.fname is '':
            return sys.stdin
        else:
            return open(self.fname)

    def readFile (self):
        with self.doOpen() as fileH:
            content = fileH.readlines()
            content = [x.strip() for x in content]
        return content

def overlap(kmerList):
    '''
    Given a list of kmers, create two separate dictionaries
    each for prefix and suffix. Then generate a dictionary of
    overlaps in the kmers and return it.
    '''
    prefixDict = {}
    suffixDict = {}
    overlapDict = {}
    for kmer in kmerList:
        prefixDict[kmer[:-1]] = kmer
        suffixDict[kmer[1:]] = kmer
    for prefix in prefixDict:
        if prefix in suffixDict:
            overlapDict[suffixDict[prefix]] = prefixDict[prefix]
    return overlapDict

def main():
    '''
    Execute overlap method and prints the overlap dictionary
    in the form of an adjacency list
    '''
    myReader = Filereader()
    kmerList = myReader.readFile()
    overlapDict = overlap(kmerList)

    for k in sorted(overlapDict):
        print(k + " -> " + overlapDict[k])

if __name__ == '__main__':
    main()
