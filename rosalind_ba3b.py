    #!/usr/bin/env python3
# Purpose: Reconstruct a String from its Genome Path

import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3b
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

def connectKmer(kmerList):
    '''
    Reconstruct a string of sequence given a list of kmers
    '''
    seq = ''
    index = 0
    for i in kmerList:
        if index == 0:
            seq += i
        else:
            seq += i[-1]
        index += 1
    return seq

def main():
    '''
    Execute connectKmer method and print the returned sequence
    '''
    myReader = Filereader()
    kmerList = myReader.readFile()
    print(connectKmer(kmerList))

if __name__ == '__main__':
    main()

    
