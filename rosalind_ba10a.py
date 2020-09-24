#!/usr/bin/env python3
# Purpose: Compute the Probability of a Hidden Path
import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba10a.
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
            content = fileH.read()
            path, states, trans = content.split('--------')
            path = path.strip()
            states = states.split()
            matrix = []
            trans = trans.strip().split('\n')[1:]
            for i in trans:
                matrix.append([float(prob) for prob in i.split()[1:]])
        return path, states, matrix

def probabilityHMM(path, states, matrix):
    '''
    Compute the probability of a hidden path.
    :param path: string representation of hidden path
    :param states: list of states in the path
    :param matrix: list of list containing probability of paths
    :return: probability of a hidden path in float
    '''
    prob = 0.5
    for i in range(len(path)-1):
        before = path[i]
        next = path[i+1]
        prob *= matrix[states.index(before)][states.index(next)]
    return prob

def main():
    '''
    parse the file and calculate the hidden path probability.
    '''
    myReader = Filereader()
    path, states, matrix = myReader.readFile()
    prob = probabilityHMM(path, states, matrix)
    print(prob)

if __name__ == '__main__':
    main()
