#!/usr/bin/env python3
# Purpose: Construct the De Bruijn Graph of a String

import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3d.
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
        return int(content[0]), content[1]


def deBruijnGraph(k, seq):
    '''
    Generate a De Bruijn Graph in a dictionary given k and sequence
    '''
    kmerDict = {}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in kmerDict:
            kmerDict[prefix] = []
            kmerDict[prefix].append(suffix)
        else:
            kmerDict[prefix].append(suffix)
    return kmerDict

def main():
    '''
    Execute deBruijnGraph method and print the graph
    in the form of an adjacency list
    '''
    myReader = Filereader()
    k, seq = myReader.readFile()
    deBruijn_Graph = deBruijnGraph(k, seq)
    for i in sorted(deBruijn_Graph):
        if deBruijn_Graph[i] != []:
            rightstr = ','.join(sorted(deBruijn_Graph[i]))
            print(i + " -> " + rightstr)

if __name__ == '__main__':
    main()
