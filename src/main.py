from os.path import dirname, abspath, realpath
import json
import yaml
import sys
import time

def mapNodeToOverrideValue(relevantBarLines, nodeTypesMap):
    nodeTypesDict = {}
    for nodetypeKey, nodetypeValue in nodeTypesMap.items():
        newNodeDict = {}
        for node in nodetypeValue:
            newNode = {}

            for line in relevantBarLines:

                if (node in line) and (" = " in line):

                    splitArray = line.rsplit(" = ", 1)
                    
                    propertyNameSplit = splitArray[0].rsplit(".", 1)
                    
                    # Handle UDP
                    if len(propertyNameSplit) == 1:
                        if "UDP" not in nodeTypesDict:
                            nodeTypesDict["UDP"] = {}            
                        if node not in nodeTypesDict["UDP"]:
                            nodeTypesDict["UDP"][node] = {}
                        nodeTypesDict["UDP"][node][propertyNameSplit[0]] = propertyValue
                    else:
                        propertyName = propertyNameSplit[1]

                        propertyValue = splitArray[1]

                        newNode[propertyName] = propertyValue
            if newNode:
                newNodeDict[node] = newNode
        if newNodeDict:
            nodeTypesDict[nodetypeKey] = newNodeDict
     
    return nodeTypesDict

def findNodeTypes(barfileLines, propertySetDict):

    # Makes ruleset into a more usable list
    
    nodeDict = {}
    
    # Makes an array that has nodenames and all their respected properties
    for line in barfileLines:

        if " = " in line:
            line = line.rsplit(" = ", 1)[0]

        if ("gen." not in line) and ("." in line):  

            splitArray = line.rsplit(".", 1)
            nodeName = splitArray[0].strip()
            propertyName = splitArray[1].strip()
            if nodeName in nodeDict:
                if propertyName not in nodeDict[nodeName]:
                    nodeDict[nodeName] += [propertyName] 
            else:
                nodeDict[nodeName] = [propertyName]
    

    nodeTypeDict = {}
    # Finds what nodes are what based on checking nodeproperties against the propertySet
    for nodeKey, nodeValue in nodeDict.items():
        sortedValue = sorted(nodeValue)
        for propertyKey, propertyValue in propertySetDict.items():
            if propertyValue == sortedValue:
    
                if propertyKey in nodeTypeDict:
                    if nodeKey not in nodeTypeDict[propertyKey]:
                        nodeTypeDict[propertyKey] += [nodeKey]
                else:
                    nodeTypeDict[propertyKey] = [nodeKey]
    
    return nodeTypeDict

def findRelevantLines(barfileLines):

    relevantLines=[]
    
    for line in barfileLines:
        if "." in line:
            relevantLines.append(line.strip())

    return sorted(relevantLines)


def formatToFileForPOC(nodeListAsDict, filePath):

    with open(filePath, "w") as file:

        file.write(json.dumps(nodeListAsDict, indent=4))


def getPropertiesFromBar(barPath, propertiesPath):
    
    with open(barPath) as barfile:
        bar =  barfile.readlines()

    with open(propertiesPath) as propfile:
        properties = yaml.safe_load(propfile)
        for propList in properties.values():
            propList = sorted(propList)

    relevantBarLines = findRelevantLines(bar)

    nodeTypesMap = findNodeTypes(relevantBarLines, properties)

    nodeTypesWithPropertyValues = mapNodeToOverrideValue(relevantBarLines, nodeTypesMap)   

    return nodeTypesWithPropertyValues

if __name__ == "__main__":
    tic = time.perf_counter()
    #TODO Fix UDP functionality
    # barPath = sys.argv[1]
    # nodePropPath = sys.argv[2]
    mainDir = dirname(realpath(dirname(realpath(__file__))))
    barPath = mainDir + "/test/Testbarfile.txt"
    nodePropPath = mainDir + "/test/node_properties.yaml"
    jsonPath = mainDir + "/test/barefileproperties.json"
    
    nodeListAsDict = getPropertiesFromBar(barPath, nodePropPath)
    toc = time.perf_counter()
    formatToFileForPOC(nodeListAsDict, jsonPath)
    print(f"Finished in {toc - tic:0.4f} seconds")

    
