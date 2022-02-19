import urllib.request, json, requests, statistics, time
from datetime import datetime
from modules import ninjaCurrencyValue, getAvgGemPrice
startTime = datetime.now()

# read weightings.json so that we can query all alt gem types
with open('weightings.json') as f:
    data = json.load(f)

# start putting prices into pricejson
for gemtype in data:
    for gem in data[gemtype]:
        for altqual in data[gemtype][gem].keys():
            if altqual == 'Superior':
                continue
            else:
                pass
            alt_price = {altqual: getAvgGemPrice(f"{altqual} {gem}")}
            data[gemtype][gem].update(alt_price)


# set file that the dictionary will be saved to
jsonfile = 'pricejson.json'
with open(jsonfile, 'w') as outfile:
    json.dump(data, outfile, indent=4)

timetakenStr = datetime.now() - startTime    
with open('../regrader_website/timetaken.txt', 'w') as x:
    x.write("Time taken to execute =")
    x.write(str(timetakenStr))