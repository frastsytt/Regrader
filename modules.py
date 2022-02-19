import requests, json, time, statistics

def ninjaCurrencyValue(league, currency):
    curValue = 0
    z = requests.get(f'https://poe.ninja/api/data/currencyoverview?league={league}&type=Currency')
    for i, currencyType in enumerate(json.loads(z.text)["lines"]):
        if currencyType['currencyTypeName'] == currency:
            curValue = json.loads(z.text)["lines"][i]["chaosEquivalent"]
            break
        else:
            continue
    return curValue

def getAvgGemPrice(gemName):
    url = f'https://www.pathofexile.com/api/trade/search/{currentLeague}'
    headers = {'User-Agent': 'Mozilla/5.0', 'content-type': 'application/json'}
    myObj = {"query": {"status": {"option": "online"}, "term": gemName,
                       "stats": [{"type": "and", "filters": []}]}, "sort": {"price": "asc"}}
    respo = json.loads(requests.post(url, data=json.dumps(myObj), headers=headers).text)

    try:
        print(respo["id"] + f" - tradelink for: {gemName}")
    except Exception as e:
        print(e)
        print(respo)
        time.sleep(60)
        return 1

    if len(respo["result"]) == 0:
        return 1

    itemList = ''
    for i, item in enumerate(respo["result"]):
        itemList += str(item) + ','
        if i > 8:
            break
    fetchurl = f"https://www.pathofexile.com/api/trade/fetch/{itemList[:-1]}?query={respo['id']}"
    avgcalc = []

    try:
        z = requests.get(fetchurl, headers=headers)
        time.sleep(0.1)
        for listingPrice in json.loads(z.text)["result"]:
            if listingPrice is None:
                continue
            elif listingPrice["listing"]["price"]["currency"] == "exalted":
                avgcalc.append(listingPrice["listing"]["price"]["amount"] * exValue)
            elif listingPrice["listing"]["price"]["currency"] == "chaos":
                avgcalc.append(listingPrice["listing"]["price"]["amount"])
            else:
                avgcalc.append(1)
                pass

        # build small dictionary to be inserted into the big dictionary
        time.sleep(10)
        return (statistics.median(avgcalc)) - 1

    except Exception as e:
        print(e)
        print(z.text)
        print("I fucked up, error msg above.")
        time.sleep(60)
        return 1

global currentLeague
currentLeague = 'Archnemesis'
global exValue
exValue = ninjaCurrencyValue(currentLeague, 'Exalted Orb')