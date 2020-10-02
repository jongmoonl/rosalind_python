#!/usr/bin/env python3
# Purpose: Implement the Viterbi Algorithm

import numpy as np
import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba10c.
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
            emissionPath, emission, states, stateList, emissionList = content.split('--------')
            emissionPath = emissionPath.strip()
            emission = emission.split()
            emission = {k: v for v, k in enumerate(emission)}
            states = states.split()
            stateList = stateList.strip().split('\n')[1:]
            stateMatrix = np.ones((len(states), len(states)))
            for i in range(len(states)):
                stateMatrix[i,:] = [float(prob) for prob in stateList[i].split()[1:]]
            emissionList = emissionList.strip().split('\n')[1:]
            emissionMatrix = np.ones((len(states), len(emission)))
            for i in range(len(states)):
                emissionMatrix[i,:] = [float(prob) for prob in emissionList[i].split()[1:]]
        return emissionPath, emission, states, stateMatrix, emissionMatrix

class hiddenMarkovModel():
    '''
    compute the forward algorithm and viterbi algorithm given
    emission path in string
    emission in list of strings
    states in list of strings
    transition table in list of list of float
    emission table in list of list of float
    '''
    def __init__(self, emissionPath, emission, states, transitionTable, emissionTable):
        self.emissionPath = emissionPath
        self.emission = emission
        self.states = states
        self.transitionTable = transitionTable
        self.emissionTable = emissionTable

    def viterbi(self):
        '''
        compute a path that maximizes the probability using viterbi algorithm
        '''
        m = np.ones((len(self.states), len(self.emissionPath) ))
        for i in range(len(m[:,0])):        # scores the first column
            m[:,0][i] = self.emissionTable[i][self.emission[self.emissionPath[0]]]
        backtrack = []                      # list containing indexes to back point towards
        for column in range(1, len(self.emissionPath)):             # for each column
            backtrackColumn = []
            for state in range(len(self.states)):                   # for each state in the column
                maxScore = 0.
                tempList = [0.]                                       # list used to keep track of index of maxScore
                for prevState in range(len(self.states)):           # state in previous node to find maxScore
                    temp = column - 1
                    score = m[prevState, temp] * self.transitionTable[prevState, state] * self.emissionTable[state, self.emission[self.emissionPath[column]]]
                    if score > maxScore:
                        maxScore = score
                        tempList.append(prevState)
                backtrackColumn.append(tempList[-1])
                m[state, column] = maxScore                         # updating the matrix with maxScore
            backtrack.append(backtrackColumn)

        #backtracking given a filled matrix
        maxPath = ''
        tempList = []                                               # list used to find index of maxScore in last nodes
        i = 0
        maxProb = 0
        for state in m:                                       
            if state[-1] > maxProb:
                maxProb = state[-1]
                tempList.append(i)
            i += 1
        bestScoreIndex = tempList[-1]
        maxPath += self.states[bestScoreIndex]
        backtrack.reverse()
        for column in backtrack:                                    # main part of backtrack
            maxPath += self.states[column[bestScoreIndex]]
            bestScoreIndex = column[bestScoreIndex]
        maxPath = maxPath[::-1]                                     # reversing the string

        return maxPath



def main():
    '''
    parse the file and calculate the path of maximum probability
    '''
    myReader = Filereader()
    emissionPath, emission, states, transitionTable, emissionTable = myReader.readFile()
    viterbi = hiddenMarkovModel(emissionPath, emission, states, transitionTable, emissionTable)
    path = viterbi.viterbi()
    print(path)


if __name__ == '__main__':
    main()
