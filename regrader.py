import urllib.request, json, requests, statistics, time
from datetime import datetime
from modules import *
startTime = datetime.now()

# read weightings.json so that we can query all alt gem types
with open('weightings.json') as f:
    data = json.load(f)

exValue = ninjaCurrencyValue('Exalted Orb')


haasBro = {}

for gemtype in data:
    insertGemType = {gemtype : {}}
    haasBro.update(insertGemType)
    print(haasBro)
    for gem in data[gemtype]:
        insertGem = {gem : {}}
        haasBro[gemtype].update(insertGem)
        print(haasBro)
        for altqual in data[gemtype][gem]["weights"].keys():
            if altqual == 'Superior':
                insertAltGem = {altqual: 1}
                haasBro[gemtype][gem].update(insertAltGem)
                print(haasBro)
                continue
            else:
                try:
                    insertAltGem = {altqual: getAvgGemPrice(f"{altqual} {gem}", exValue)[0]}
                    haasBro[gemtype][gem].update(insertAltGem)
                    print(haasBro)
                except Exception as e:
                    sleepError(e)

haasJson = 'haasBroJson.json'
with open(haasJson, 'w') as outfile:
    json.dump(haasBro, outfile, indent=4)


# start putting prices into pricejson
for gemtype in data:
    for gem in data[gemtype]:
        for altqual in data[gemtype][gem]["weights"].keys():
            if altqual == 'Superior':
                continue
            else:
                try:
                    alt_price = {"marketValue": getAvgGemPrice(f"{altqual} {gem}", exValue)[0]}
                    data[gemtype][gem]["weights"][altqual].update(alt_price)
                    tradelink = {"tradeLink": getAvgGemPrice(f"{altqual} {gem}", exValue)[1]}
                    data[gemtype][gem]["weights"][altqual].update(alt_price)
                    print(alt_price)
                except Exception as e:
                    sleepError(e)



# set file that the dictionary will be saved to
jsonfile = 'pricejson.json'
with open(jsonfile, 'w') as outfile:
    json.dump(data, outfile, indent=4)

timetakenStr = datetime.now() - startTime    
with open('../regrader_website/timetaken.txt', 'w') as x:
    x.write("Time taken to execute =")
    x.write(str(timetakenStr))