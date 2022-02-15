from distutils.text_file import TextFile
import urllib.request, json, requests, statistics, time
from heapq import nlargest
import numpy as np
import pandas as pd


# read weightings.json so that we can query all alt gem types
with open('weightings.json') as f:
    dataWeight = json.load(f)
with open('pricejson.json') as f:
    dataPrice = json.load(f)

weightList = []
primeregradingPrice = 70
secondaryregradingPrice = 70

data_set = {}

#For loop, goes through all gems and their alt qualities and instantly converts that into possible profit.
for gemtype in dataWeight:
    for gem in dataWeight[gemtype]:
        qual1weightprofit = 0
        qual2weightprofit = 0
        qual3weightprofit = 0
        qual1 = 0
        qual2 = 0
        qual3 = 0
        qualtotal = 0
        count = 0
        totalprofit = 0
        if(gem == "Item Quantity Support"):
            break;
        for altqual in dataWeight[gemtype][gem]:
            if(altqual != "Superior"):
                try:
                    if(altqual == "Divergent"):
                        qual1 = int(dataWeight[gemtype][gem][altqual])
                    if(altqual == "Anomalous"):
                        qual2 = int(dataWeight[gemtype][gem][altqual])
                    if(altqual == "Phantasmal"):
                        qual3 = int(dataWeight[gemtype][gem][altqual])
                    count += 1
                except Exception as e:
                    print(e)
                    pass
            else:
                continue
        #Add together all weights and then devide the seperate weights to get the chance to hit each one.
        qualtotal = qual1 + qual2 + qual3
        qual1weight = qual1 / qualtotal
        qual2weight = qual2 / qualtotal
        qual3weight = qual3 / qualtotal

        #Multiply all chances with the corresponding price to see how much money you get on average for each hit.
        if(qual1weight != 0):
            qual1weightprofit = qual1weight * dataPrice[gemtype][gem]["Divergent"]
        if(qual2weight != 0):
            qual2weightprofit = qual2weight * dataPrice[gemtype][gem]["Anomalous"]
        if(qual3weight != 0):
            qual3weightprofit = qual3weight * dataPrice[gemtype][gem]["Phantasmal"]

        #Add together all the prices to figure out your average profit.
        if(gemtype == "active"):
            totalprofit = (qual1weightprofit + qual2weightprofit + qual3weightprofit) - primeregradingPrice
        if(gemtype == "support"):
            totalprofit = (qual1weightprofit + qual2weightprofit + qual3weightprofit) - secondaryregradingPrice

        object = {gem : totalprofit}
        data_set.update(object)
        weightList.append(str(totalprofit) + gem)

s = pd.Series(data_set)
s = s.nlargest(len(s), keep = 'all')
f = s.to_dict()
jsonfile = 'profit.json'
with open(jsonfile, 'w') as outfile:
    json.dump(f, outfile, indent=4)

weightFile = open("weightList.txt", "w")
for element in weightList:
    weightFile.write(str(element) + "\n")
weightFile.close
