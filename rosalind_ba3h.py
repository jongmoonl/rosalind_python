#!/usr/bin/env python3
# Purpose: Reconstruct a String from its k-mer Composition

import sys
import random

class Filereader :
    '''
    Reads a file then parses the data
    necessary for rosalind problem ba3h.
    '''
    def __init__ (self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname

    def doOpen (self):
        if self.fname == '':
            return sys.stdin
        else:
            return open(self.fname)

    def readFile (self):
        with self.doOpen() as fileH:
            content = fileH.readlines()
            content = [x.strip() for x in content]
        return content[1:], content[0]

class graphicalMethods:
    '''
    Takes in a specified length of kmer and list of kmers
    deBruijnGraph method generates and returns an adjacency dictionary
    makeCycle method converts a graph containing eulerian path to a graph containing eulerian cycle
    and returns the first node of the graph.
    eulerianCycle method finds a eulerian cycle in a balanced graph and returns
    a reconstructed string given a balanced graph of kmer composition and the first node.
    '''
    def __init__(self, kmerList, k):
        self.kmerList = kmerList
        self.k = k

    def deBruijnGraph(self, seq):
        '''
        create an adjacency of prefix and suffix of a kmer given a list of kmers
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

    def makeCycle(self, graph):
        '''
        Given a directed graph that contains Eulerian path,
        connects the last node to the start node by adding an edge
        '''
        counter = {}
        for left in graph:
            if left not in counter:
                counter[left] = [0, len(graph[left])]
            else:
                counter[left][1] += len(graph[left])
            for right in graph[left]:
                if right not in counter:
                    counter[right] = [1, 0]
                else:
                    counter[right][0] += 1
        start, end = '', ''
        for i in counter:
            if counter[i][0] - counter[i][1] < 0:
                start = i
            if counter[i][0] - counter[i][1] > 0:
                end = i
        if end in graph:
            graph[end].append(start)
        else:
            graph[end] = [start]
        return start, end

    def eulerianCycle(self, balancedGraph, first):
        '''
        Create an eulerian cycle by traversing through edges
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
                            #print("TRAVERSING...", current, ":", balancedGraph[current])
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
        result = first[:-1]
        for i in path:
            result += i[-1]                                             # concatenate one base per edge
        return result

def main():
    '''
    take in a rosalind ba3h file and parse the input containing kmer size amd kmer list
    then utilizes methods in class graphicalMethods.
    find a eulerian cycle in the given balanced graph made with deBruijnGraph method
    and prints the reconstructed string.
    '''
    myReader = Filereader()
    kmerList, k = myReader.readFile()
    reconstruct = graphicalMethods(kmerList, k)
    deBruijn_Graph = reconstruct.deBruijnGraph(kmerList)
    first, last = reconstruct.makeCycle(deBruijn_Graph)
    print(reconstruct.eulerianCycle(deBruijn_Graph, first))

if __name__ == '__main__':
    main()
