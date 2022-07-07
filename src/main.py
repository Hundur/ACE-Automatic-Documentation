from os.path import dirname, abspath
import json

def mapNodeToOverrideValue(relevantBarLines, nodeTypesMap):

    nodeTypeIndex = -1

    for nodeType in nodeTypesMap:

        nodeTypeIndex = nodeTypeIndex + 1
        newNodeArray = []

        for node in nodeType[1]:
            
            newNode = ["", []]
            hasPropertyValue = False

            newNode[0] = node[0]

            for line in relevantBarLines:

                if (node[0] in line) and (" = " in line) and ("." in line):

                    splitArray = line.rsplit(" = ", 1)
                    propertyName = splitArray[0].rsplit(".", 1)[1]
                    propertyValue = splitArray[1]

                    propertyNameValue = propertyName + " = " + propertyValue

                    if (newNode[1].count(propertyNameValue) == 0):
                        newNode[1].append(propertyNameValue)
                        hasPropertyValue = True

            if hasPropertyValue:
               newNodeArray.append(newNode)

        nodeTypesMap[nodeTypeIndex][1] = newNodeArray

    return nodeTypesMap

def findNodeTypes(barfileLines, propertySetLines):

    listIndex = -1
    propertySetList = []

    # Makes ruleset into a more usable list
    for line in propertySetLines:
        if ":" in line:
            listIndex = listIndex + 1
            propertySetList.append([line.split(":")[0], []])
        else:
            propertySetList[listIndex][1].append(line.strip())

    firstEntry = True
    listIndex = -1
    nodeList = []

    # Makes an array that has nodenames and all their respected properties
    for line in barfileLines:

        if " = " in line:
            line = line.rsplit(" = ", 1)[0]

        if ("gen." not in line) and ("." in line):  

            splitArray = line.rsplit(".", 1)
            nodeName = splitArray[0].strip()
            propertyName = splitArray[1].strip()

            if firstEntry:
                currentName = nodeName
                firstEntry = False

                listIndex = listIndex + 1
                nodeList.append([nodeName, []])
            
            if currentName != nodeName:
                currentName = nodeName

                listIndex = listIndex + 1
                nodeList.append([nodeName, []])

            if nodeList[listIndex][1].count(propertyName) == 0:
                nodeList[listIndex][1].append(propertyName)

    nodeTypeList = []
    existsInArray = False

    # Finds what nodes are what based on checking nodeproperties against the propertySet
    for node in nodeList:
        for propertySet in propertySetList:

            if node[1] == propertySet[1]:

                existsInArray = False
                listIndex = -1

                for item in nodeTypeList:

                    listIndex = listIndex + 1

                    if item[0] == propertySet[0]:
                        existsInArray = True
                        nodeTypeList[listIndex][1].append([node[0], []])

                if not existsInArray:
                    nodeTypeList.append([propertySet[0], [[node[0], []]]])

    return nodeTypeList

def findRelevantLines(barfileLines):

    relevantLines=[]
    
    for line in barfileLines:
        if "." in line:
            relevantLines.append(line.strip())

    return sorted(relevantLines)

def writeDocToFile(filePath, txtToWriteArray):

    rootDir = dirname(dirname(abspath(__file__)))

    with open(rootDir + filePath, "w") as file:
        for item in txtToWriteArray:
            file.write("%s\n" % item)

def readFile(filePath):

    rootDir = dirname(dirname(abspath(__file__)))   
    barfile = open(rootDir + filePath, "r")

    return barfile.readlines()

def formatToFileForPOC(nodeListAsDict, filePath):

    rootDir = dirname(dirname(abspath(__file__)))

    with open(rootDir + filePath, "w") as file:

        file.write(json.dumps(nodeListAsDict))

def nodelist_to_dict(arr):

    nodelist = arr
    node_dict = {}

    for line in nodelist:
        node_dict[line[0]] = line[1]

    for key, value in node_dict.items():

        value_dict = {}

        for k, v in value:

            value_dict[k] = v

        for k, v in value_dict.items():

            prop_dict = {}

            for element in v:

                split = element.split(" = ")
                prop_dict[split[0]] = split[1]

            value_dict[k] = prop_dict

        node_dict[key] = value_dict

    return node_dict

if __name__ == "__main__":

    #TODO Fix UDP functionality

    barfileLines = readFile("/test/Testbarfile.txt")
    nodePropertySetLines = readFile("/test/NodePropertiesRuleset.txt")
    
    relevantBarLines = findRelevantLines(barfileLines)

    nodeTypesMap = findNodeTypes(relevantBarLines, nodePropertySetLines)

    nodeTypesWithPropertyValues = mapNodeToOverrideValue(relevantBarLines, nodeTypesMap)   

    nodeListAsDict = nodelist_to_dict(nodeTypesWithPropertyValues)

    formatToFileForPOC(nodeListAsDict, "/test/test.txt")