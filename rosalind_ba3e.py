#!/usr/bin/env python4
# Purpose: Construct the De Bruijn Graph of a Collection of k-mers

import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3e.
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

def deBruijnGraph(seq):
    '''
    Generate De Bruijn Graph from list of kmers and
    return
    '''
    kmerDict = {}
    for motif in seq:
        prefix = motif[:-1]
        suffix = motif[1:]
        if prefix not in kmerDict:
            kmerDict[prefix] = []
            kmerDict[prefix].append(suffix)
        else:
            kmerDict[prefix].append(suffix)
    return kmerDict

def main():
    '''
    Execute method deBruijnGraph with a given file
    and prints the graph in the form of adjacency list
    '''
    myReader = Filereader()
    kmerList = myReader.readFile()
    deBruijn_Graph = deBruijnGraph(kmerList)

    for i in sorted(deBruijn_Graph):
        if deBruijn_Graph[i] != []:
            rightstr = ','.join(sorted(deBruijn_Graph[i]))
            print(i + " -> " + rightstr)


if __name__ == '__main__':
    main()
