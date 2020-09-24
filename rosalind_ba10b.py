#!/usr/bin/env python3
# Purpose: Compute the Probability of an Outcome Given a Hidden Path
import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba10b
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
            path, states, hiddenPath, hiddenState, trans = content.split('--------')
            path = path.strip()
            states = states.split()
            hiddenPath = hiddenPath.strip()
            hiddenState = hiddenState.split()
            matrix = []
            trans = trans.strip().split('\n')[1:]
            for i in trans:
                matrix.append([float(prob) for prob in i.split()[1:]])
        return path, states, hiddenPath, hiddenState, matrix

def probabilityHMM(path, states, hiddenPath, hiddenState, matrix):
    '''
    Compute the Probability of an Outcome Given a Hidden Path
    :param path: string representation of path
    :param states: list of states in the path
    :param hiddenPath: string representation of hidden path
    :param hiddenState: list of hidden states in the hidden path
    :param matrix: list of list containing probability of paths
    :return: probability of a hidden path in float
    '''
    prob = 1.
    for i in range(len(path)):
        character = path[i]
        state = hiddenPath[i]
        prob *= matrix[hiddenState.index(state)][states.index(character)]
    return prob


def main():
    '''
    parse the file and calculate the probability of an outcome.
    '''
    myReader = Filereader()
    path, states, hiddenPath, hiddenState, matrix = myReader.readFile()
    prob = probabilityHMM(path, states, hiddenPath, hiddenState, matrix)
    print(prob)

if __name__ == '__main__':
    main()
