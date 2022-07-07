from os.path import dirname, abspath

def mapNodeToOverrideValue(relevantBarLines, nodeTypesMap):

    for nodeType in nodeTypesMap:

        newPropertiesArray = []

        for node in nodeType[1]:

            for line in relevantBarLines:

                if (node[0] in line) and (" = " in line) and ("." in line):

                    splitArray = line.rsplit(" = ", 1)
                    propertyName = splitArray[0].rsplit(".", 1)[1]
                    propertyValue = splitArray[1]

                    propertyNameValue = propertyName + " = " + propertyValue

                    if (node[1].count(propertyNameValue) == 0):
                        newPropertiesArray.append(propertyNameValue)

            node[1] = newPropertiesArray
                    
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
        if "propertyIdentifier" and "#" in line:
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

if __name__ == "__main__":

    #TODO Fix UDP functionality

    barfileLines = readFile("/test/Testbarfile.txt")
    nodePropertySetLines = readFile("/test/NodePropertiesRuleset.txt")
    
    relevantBarLines = findRelevantLines(barfileLines)

    nodeTypesMap = findNodeTypes(relevantBarLines, nodePropertySetLines)

    nodeTypesWithPropertyValues = mapNodeToOverrideValue(relevantBarLines, nodeTypesMap)   

    writeDocToFile("/test/test.txt", nodeTypesWithPropertyValues)

