import re
from itertools import combinations

# ========================================
# File Reading 
# ========================================


categoriesFile = 'categories.txt'

#takes filepath of text file and returns it as line by line list
def fileScan(filePath):
    lineList = []
    with open(filePath, 'r') as file:
        for line in file:
            lineList.append(line.strip())
    return lineList


lineList = fileScan(categoriesFile)

# ========================================
# Splits each line into a list of words
# ========================================

#takes line and splits it according the rule into a list of segments
def wordSplit(line, splitRule):
    lineWords = re.split(splitRule, line)
    return lineWords

splitRule = r'[;]+'

lineList2 = []
for line in lineList:
    lineList2.append(wordSplit(line, splitRule))

lineList = lineList2


# ========================================
# 1-Itemset
# ========================================


#returns a dictionary of all single terms in document and their counts
def termInitialize(lineList):
    categoryDict = {}

    for line in lineList:
        for word in line:
            if(word in categoryDict):
                categoryDict[word] = categoryDict[word] + 1
            else:
                categoryDict[word] = 1
    return categoryDict

categoryDict = termInitialize(lineList)

filtered_dict = {name: frequency for name, frequency in categoryDict.items() if frequency >= 771.85}
print(filtered_dict)

def dictToSet(dict):
    frequent1Itemsets = set()
    for item in dict.keys():
        frequent1Itemsets.add(frozenset([item]))
    return frequent1Itemsets

filtered_set = dictToSet(filtered_dict)
print(filtered_set)




# ========================================
# N-Itemset
# ========================================

def termJoins(prevFrequentItems, kLength):
    newCandidates = set()
    for set1 in prevFrequentItems:
        for set2 in prevFrequentItems:
            unionSet = set1.union(set2)
            if(len(unionSet) == kLength):
                newCandidates.add(frozenset(unionSet))
    return newCandidates




newSet = termJoins(filtered_set, 2)




def genPruningSubsets(candidate, length):
    combos = combinations(candidate, length)
    pruningSubsets = set()
    for combo in combos:
        pruningSubsets.add(frozenset(combo))
    return pruningSubsets

def prune(candidateSet, length, prevFrequentItems):
    prunedCandidates = set()
    for candidate in candidateSet:
        pruningSubsets = genPruningSubsets(candidate, length-1)
        if all(subset in prevFrequentItems for subset in pruningSubsets):
            prunedCandidates.add(candidate)
    return prunedCandidates
    
newSet = prune(newSet, 2, filtered_set)




def supCount(candidate, lineList):
    count = 0
    for line in lineList:
        lineSet = set(line)
        if(candidate.issubset(lineSet)):
            count += 1
    return count

def minSup(candidateSet, lineList, supThres, file):
    trueFrequentSet = set()
    k = 0
    for candidate in candidateSet:
        count = supCount(candidate, lineList)

        if(count >= supThres):
            k += 1
            trueFrequentSet.add(candidate)
            print('count ', count)
            print(candidate)
            print('k', k)
            if file != None:
                inputString = str(count) + ":"
                for category in candidate:
                    inputString += (category + ";")
                inputString = inputString[:-1] + "\n"
                file.write(inputString)
    
    return trueFrequentSet

trueSet = minSup(newSet, lineList, 771.85, None)
print(trueSet)
print(len(trueSet))
print(len(newSet))




def aprioriLoop(lineList, minSupThres, frequentOneItemsets, finalFrequentItemsets, file):
    itemSetLength = 2
    prevFrequentItemsets = frequentOneItemsets

    while(len(prevFrequentItemsets) > 0):
        #generate candidate itemsets of size itemSetLength by joining size itemSetLength - 1 itemsets
        candidateItemsets = termJoins(prevFrequentItemsets, itemSetLength)
        #prune candidates based on their subsets
        prunedCandidates = prune(candidateItemsets, itemSetLength, prevFrequentItemsets)
        #check minimum support and eliminate infrequent
        currentFrequentItemsets = minSup(prunedCandidates, lineList, minSupThres, file)
        #add current length frequent itemsets to final list
        finalFrequentItemsets.update(currentFrequentItemsets)
        print(str(itemSetLength) + " length sets " + str(len(currentFrequentItemsets)))

        #increment 
        itemSetLength += 1
        prevFrequentItemsets = currentFrequentItemsets
        print('itemSetLength', itemSetLength)





def apriori(lineList, minSupThres, fileName):
    # Open the file in write mode ('w')
    with open(fileName, 'w') as file:

        finalFrequentItemsets = set()

        termDict = termInitialize(lineList)
        frequentTerms = {name: frequency for name, frequency in termDict.items() if frequency >= minSupThres}
        frequentOneItemsets = dictToSet(frequentTerms)

        for key in frequentTerms:
            file.write(f"{frequentTerms[key]}:{key}\n")

        finalFrequentItemsets.update(frequentOneItemsets)

        aprioriLoop(lineList, minSupThres, frequentOneItemsets, finalFrequentItemsets, file)

    print(finalFrequentItemsets)


# categoryDict = termInitialize(lineList)

# filtered_dict = {name: frequency for name, frequency in categoryDict.items() if frequency >= 771.85}

# print(filtered_dict)

# # Open the file in write mode ('w')
# with open('patterns.txt', 'w') as file:
#     for key in filtered_dict:
#         print(f"{filtered_dict[key]}:{key}")
#         file.write(f"{filtered_dict[key]}:{key}\n")


apriori(lineList, 771.85, 'patterns.txt')