#!/usr/bin/env python3
# Purpose: Reconstruct a String from its k-mer Composition

import numpy as np

def readFile(file):
    '''
    designed to read a rosalind ba5d input then
    parse to return a graph, sink and source
    '''
    with open(file) as f:
        content = f.read()
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

class viterbiAlgorithm():
    def __init__(self, emissionPath, emission, states, transitionTable, emissionTable):
        self.emissionPath = emissionPath
        self.emission = emission
        self.states = states
        self.transitionTable = transitionTable
        self.emissionTable = emissionTable

    def printObject(self):
        print('EMISSION PATH:', self.emissionPath)
        print('EMISSION:', self.emission)
        print('STATES:', self.states, '\n')
        print('TRANSITION TABLE')
        for i in self.transitionTable:
            print(i)
        print()
        print('EMISSION TABLE')
        for i in self.emissionTable:
            print(i)
        print()

    def viterbi(self):
        print('----------------------------\n', self.emission)

        m = np.ones((len(self.states), len(self.emissionPath) ))
        for i in range(len(m[:,0])):        # scores the first column
            m[:,0][i] = self.emissionTable[i][self.emission[self.emissionPath[0]]]
        print(m)
        backtrack = []
        for column in range(1, len(self.emissionPath)):
            print()
            print('CURRENTLY IN COLUMN...', column, self.emissionPath[column])
            backtrackColumn = []
            for state in range(len(self.states)):
                print('\t CURRENTLY IN STATE...', self.states[state], 'OF COLUMN...', column, self.emissionPath[column])
                maxScore = 0.
                tempList = [0.]
                for prevState in range(len(self.states)):
                    temp = column - 1
                    print('\t\t CURRENTLY IN STATE...', self.states[prevState], 'OF COLUMN...', temp, self.emissionPath[temp])
                    score = m[prevState, temp] * self.transitionTable[prevState, state] * self.emissionTable[state, self.emission[self.emissionPath[column]]]
                    print('\t\t\t SCORE HERE IS...', score, '=', m[prevState, temp], '*', self.transitionTable[prevState, state], '*', self.emissionTable[state, self.emission[self.emissionPath[column]]])
                    if score > maxScore:
                        maxScore = score
                        tempList.append(prevState)
                backtrackColumn.append(tempList[-1])
                print('\t\t MAX SCORE IS...', maxScore)
                m[state, column] = maxScore
            backtrack.append(backtrackColumn)
        print(m)
        print(backtrack)

        maxPath = ''
        tempList = []
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
        print(backtrack)

        for column in backtrack:
            maxPath += self.states[column[bestScoreIndex]]
            bestScoreIndex = column[bestScoreIndex]
        maxPath = maxPath[::-1]
        print(maxPath)




def main():
    emissionPath, emission, states, transitionTable, emissionTable = readFile('problem18.txt')
    #emissionPath, emission, states, transitionTable, emissionTable = readFile('rosalind_ba10c.txt')
    viterbi = viterbiAlgorithm(emissionPath, emission, states, transitionTable, emissionTable)
    viterbi.printObject()
    viterbi.viterbi()



if __name__ == '__main__':
    main()
