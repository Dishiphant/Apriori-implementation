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

filtered_dict = {name: frequency for name, frequency in categoryDict.items() if frequency > 771}
# print(filtered_dict)

def dictToSet(dict):
    frequent1Itemsets = set()
    for item in dict.keys():
        frequent1Itemsets.add(frozenset([item]))
    return frequent1Itemsets

filtered_set = dictToSet(filtered_dict)
# print(filtered_set)




# ========================================
# N-Itemset
# ========================================

def termJoins(prevFrequentItems, kLength):
    newCandidates = set()
    for set1 in prevFrequentItems:
        for set2 in prevFrequentItems:
            joinSet = set(set1.union(set2))
            if(len(joinSet) == kLength):
                newCandidates.add(frozenset(joinSet))
    return newCandidates




newSet = termJoins(filtered_set, 2)




def genPruningSubsets(candidate, length):
    combos = combinations(candidate, length)
    pruningSubsets = set()
    for combo in combos:
        pruningSubsets.add(frozenset(combo))
    return pruningSubsets

def prune(candidateSet, length, prevFrequentItems):
    for candidate in candidateSet:
        pruningSubsets = genPruningSubsets(candidate, length-1)
        prunedCandidates = {candidate for candidate in candidateSet if all(subset in prevFrequentItems for subset in pruningSubsets)}
        return prunedCandidates
    
newSet = prune(newSet, 2, filtered_set)




def supCount(candidate, lineList):
    count = 0
    for line in lineList:
        lineSet = set(line)
        if(candidate.issubset(lineSet)):
            count += 1
    return count

def minSup(candidateSet, lineList, supThres):
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
    
    return trueFrequentSet

trueSet = minSup(newSet, lineList, 771)
print(trueSet)
print(len(trueSet))
print(len(newSet))




def aprioriLoop(document, minSupThres, frequentOneItemsets, finalFrequentItemsets):
    itemSetLength = 2
    prevFrequentItemsets = frequentOneItemsets

    #generate candidate itemsets of size itemSetLength by joining size itemSetLength - 1 itemsets
    candidateItemsets = termJoins(prevFrequentItemsets, itemSetLength)
    #prune candidates based on their subsets
    prunedCandidates = prune(candidateItemsets, itemSetLength, prevFrequentItemsets)
    #check minimum support and eliminate infrequent
    currentFrequentItemsets = minSup(prunedCandidates, document, minSupThres)

    finalFrequentItemsets.update(currentFrequentItemsets)

    #repeat
    itemSetLength += 1
    prevFrequentItemsets = currentFrequentItemsets





def apriori(document, minSupThres):
    finalFrequentItemsets = set()

    termDict = termInitialize(lineList)
    frequentTerms = {name: frequency for name, frequency in termDict.items() if frequency >= minSupThres}
    frequentOneItemsets = dictToSet(frequentTerms)

    finalFrequentItemsets.update(frequentOneItemsets)

    aprioriLoop()











# #gets list of terms from list of lines

# def termInitialize(lineList):
#     categoryDict = {}

#     for line in lineList:
#         lineWords = wordSplit(line, splitRule)
#         for term in lineWords:
#             termList = list()
#             termList.append(term)
#             if(termList in categoryDict):
#                 categoryDict[termList] = categoryDict[termList] + 1
#             else:
#                 categoryDict[termList] = 1
#     return categoryDict

# categoryDict = termInitialize(lineList)

# print(categoryDict)

# # filtered_dict = {name: frequency for name, frequency in categoryDict.items() if frequency > 771}
# # print(filtered_dict)

# # def patternDictionary(lineList, candidateList):
# #     patternDict = {}
# #     for line in lineList:
# #         lineWords = wordSplit(line, splitRule)
# #         if (for all term in candidateList) term in lineWords:


# #         for term in lineWords:
# #             if(term in categoryDict):
# #                 categoryDict[term] = categoryDict[term] + 1
# #             else:
# #                 categoryDict[term] = 1
# #     return categoryDict




