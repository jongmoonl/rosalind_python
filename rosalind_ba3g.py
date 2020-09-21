#!/usr/bin/env python3
# Purpose: Find an Eulerian Path in a Graph

import random
import sys

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3g.
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
            connect = {}
            for i in content:
                prefix, suffixes = i.strip().split(' -> ')
                suffix = list(suffixes.split(','))
                connect[prefix] = suffix
        return connect

class eulerianPath:
    '''
    Given a directed path containing an Eulerian path,
    makeCycle converts eulerian path to eulerian cycle and
    eulerianCycle finds and returns a eulerian cycle given a directed graph
    containing eulerian cycle.
    '''

    def __init__(self, adjacencyDict):
        self.seq = adjacencyDict

    def makeCycle(self, graph):
        '''
        Given a directed graph that contains Eulerian path,
        connects the last node to the start node by adding an edge
        '''
        counter = {}                                    # Counts incoming edge and outgoing edge for each node

        for left in graph:
            if left not in counter:
                counter[left] = [0, len(graph[left])]   # [incoming edge n , outgoing edge n]
            else:
                counter[left][1] += len(graph[left])
            for right in graph[left]:
                if right not in counter:
                    counter[right] = [1, 0]
                else:
                    counter[right][0] += 1
        start, end = '', ''                             # start and end node
        for i in counter:
            if counter[i][0] - counter[i][1] < 0:       # if outgoing edge > incoming edge
                start = i                               # then start node
            if counter[i][0] - counter[i][1] > 0:       # if incoming edge > outgoing edge
                end = i                                 # then end node

        if end in graph:
            graph[end].append(start)
        else:
            graph[end] = [start]
        return start, end

    def eulerianCycle(self, balancedGraph, first):
        '''
        Create anv eulerian cycle by traversing through edges
        when cycle is found, looks for a node with unused edge
        to create a new cycle and combine cycles.
        Keeps the first node from input to turn eulerian cycle into eulerian path
        '''
        start = random.choice(sorted(list(balancedGraph.keys())))       # randomly select a key
        cycle = []
        current = balancedGraph[start].pop()                            # pop the value for the start
        while current != start:                                         # traverse until you reach start node
            cycle.append(current)
            current = balancedGraph[current].pop(random.randrange(len(balancedGraph[current])))
                                                                        # randomly select an outgoing edge
        cycle.append(current)                                           # completes the first cycle

        while len(balancedGraph) != 0:                                  # checks if every edge has been used
            for node in cycle:                                          # for every node in the cycle
                if node in balancedGraph:
                    if balancedGraph[node] != []:                       # if outgoing edges exist
                        newCycle = []                                   # create a new cycle and traverse
                        current = balancedGraph[node].pop()
                        start = node
                        while current != start:
                            newCycle.append(current)
                            current = balancedGraph[current].pop()
                        newCycle.append(start)
                        index = cycle.index(node)
                        cycle = cycle[:index+1] + newCycle + cycle[index+1:]
                                                                        # insert the new cycle
                removeList = []
                for node in balancedGraph:
                    if len(balancedGraph[node]) == 0:
                        removeList.append(node)
                for node in removeList:
                    del balancedGraph[node]                             # cleaning the dict to check remove keys

        index = cycle.index(first)                                      # index to start from first node
        path = cycle[index:] + cycle[:index]                            # and convert cycle to path
        result = ''
        for i in path:
            result += i + '->'
        result = result[:-2]                                            # removing the last '->'
        return result



def main():
    '''
    Create eulerianPath class then execute makeCycle and eulerianCycle
    methods to create and print an eulerian path in the graph
    '''
    myReader = Filereader()
    adjacencyDict = myReader.readFile()
    ep = eulerianPath(adjacencyDict)
    first, last = ep.makeCycle(adjacencyDict)
    print(ep.eulerianCycle(adjacencyDict, first))


if __name__ == '__main__':
    main()
