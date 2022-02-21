import urllib.request, json, requests, statistics, time
from datetime import datetime
from modules import *
startTime = datetime.now()

# read weightings.json so that we can query all alt gem types
with open('weightings.json') as f:
    data = json.load(f)

exValue = ninjaCurrencyValue('Exalted Orb')

# start putting prices into pricejson
for gemtype in data:
    for gem in data[gemtype]:
        for altqual in data[gemtype][gem]["weights"].keys():
            if altqual == 'Superior':
                continue
            else:
                try:
                    alt_price = {"marketValue": getAvgGemPrice(f"{altqual} {gem}", exValue)}
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