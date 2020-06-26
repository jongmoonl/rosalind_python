#!/usr/bin/env python3
# Purpose: Generate the k-mer Composition of a String


import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3a
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


def kmerList(seq, k):
    '''
    Given a sequence in string and k in integer,
    generate list of kmers in the sequence and return
    '''
    kmerList = []
    for i in range(len(seq)-k+1):
        kmerList.append(seq[i:i+k])
    return kmerList


def main():
    '''
    Execute kmerList method and print each kmer
    '''
    myReader = Filereader()
    k, seq = myReader.readFile()
    kmerL = kmerList(seq, k)

    for kmer in kmerL:
        print(kmer)


if __name__ == '__main__':
    main()

