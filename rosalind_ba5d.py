#!/usr/bin/env python3
import math
import sys

class Filereader :

    def __init__ (self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname

    def doOpen (self):
        if self.fname is '':
            return sys.stdin
        else:
            return open(self.fname)

    def readFile (self):
        '''
        Reads a file then parses the data
        necessary for rosalind problem ba5d
        Returns source, sink and graph
        graph = { node : {nextNode : weight, nextNode : weight, ...} }
        '''
        with self.doOpen() as fileH:
            content = fileH.readlines()
            content = [x.strip() for x in content]
            source = content[0]
            sink = content[1]
            graph = {}
            for i in content[2:]:
                node, next = i.strip().split('->')
                next, weight = next.split(':')
                weight = int(weight)        # distinguishing weight as int and node as str
                if node not in graph:       # if node is not already in graph
                    graph[node] = {}        # create a dict for the node in graph
                graph[node][next] = weight
        return source, sink, graph

def topologicalOrdering(graph):
    '''
    creates a topological order by checking each node
    for any incoming edges
    '''
    tplist = []             # List for topological ordering
    candidates = []         # List for nodes without incoming edges
    inv_graph = {}
    for k, v in graph.items():              # Create inverse graph
        for key, value in v.items():
            if key in inv_graph:
                inv_graph[key][k] = value
            else:
                inv_graph[key] = {}
                inv_graph[key][k] = value
    for node in graph:                  # appending nodes without incoming edges
        if node not in inv_graph:
            candidates.append(node)
    while candidates:                     # while the list of node without incoming edge is not empty
        a = candidates.pop(-1)            # pops the node then remove all the edges from the node
        tplist.append(a)
        if a in graph:
            for key in graph[a].keys():
                inv_graph[key].pop(a)
                if inv_graph[key] == {}:
                    inv_graph.pop(key)
                if key not in inv_graph:
                    candidates.append(key)
    return tplist

def longestPath(graph, source, sink):
    '''
    utilizes topological order method to find a longest path in a
    directed acyclic graph.
    first sets all nodes except the source to negative infinity,
    then goes through a topological order list to assign scores
    Once the scoring is done, the path is found through backtracking
    '''
    inv_graph = {}                  # creating inverse graph
    for k, v in graph.items():
        for key, value in v.items():
            if key in inv_graph:
                inv_graph[key][k] = value
            else:
                inv_graph[key] = {}
                inv_graph[key][k] = value

    score = {}
    for node in graph:              # setting the scores to -inf
        score[node] = -math.inf
    score[source] = 0

    ordered = topologicalOrdering(graph)    # ordered = list of nodes in topological order

    for node in ordered:
        tempScoreList = []
        if node in score:
            tempScoreList.append([score[node],node])
        if node in inv_graph:               # if incoming edge exists
            for inc in inv_graph[node]:     # calculate node + edge score for each incoming edge
                tempScore = score[inc][0] + inv_graph[node][inc]    # [score, backtrack pointer]
                tempScore = [tempScore,inc]
                tempScoreList.append(tempScore)
        if tempScoreList:
            score[node] = max(tempScoreList)    # then find the max of note + edge

    backtrackPoint = sink
    backtrackList = []
    backtrackList.append(backtrackPoint)
    while backtrackPoint != source:
        backtrackPoint = score[backtrackPoint][1]
        backtrackList.append(backtrackPoint)

    backtrackList.reverse()             # reversing the list from sink to source
    return backtrackList, score[sink][0]

def main():
    myReader = Filereader()
    source, sink, graph = myReader.readFile()
    backtrackList, sinkScore = longestPath(graph, source, sink)
    print(sinkScore)
    print('->'.join(backtrackList))


if __name__ == '__main__':
    main()
