import requests, json, time, statistics

currentLeague = 'Archnemesis'

def ninjaCurrencyValue(currency, league = currentLeague):
    curValue = 0
    z = requests.get(f'https://poe.ninja/api/data/currencyoverview?league={league}&type=Currency')
    for i, currencyType in enumerate(json.loads(z.text)["lines"]):
        if currencyType['currencyTypeName'] == currency:
            curValue = json.loads(z.text)["lines"][i]["chaosEquivalent"]
            break
        else:
            continue
    return curValue

def getAvgGemPrice(gemName, exValue, corrFlag=False):
    url = f'https://www.pathofexile.com/api/trade/search/{currentLeague}'
    headers = {'User-Agent': 'Regrader/1.0 roomet.sytt@voco.ee guki#7589 https://github.com/frastsytt/Regrader', 'content-type': 'application/json'}
    myObj = {"query":{"status":{"option":"online"},"term": gemName,"stats":[{"type":"and","filters":[]}],"filters":{"misc_filters":{"filters":{"corrupted":{"option":corrFlag}}}}},"sort":{"price":"asc"}}

    try:
        respo = json.loads(requests.post(url, data=json.dumps(myObj), headers=headers).text)
        print(respo["id"] + f" - tradelink for: {gemName}")
    except Exception as e:
        print(e)
        print(myObj)
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
    print(fetchurl)
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



        # build small dictionary to be inserted into the big dictionary
        time.sleep(10)
        return (statistics.median(avgcalc)) - 1

    except Exception as e:
        print(e)
        print(z.text)
        print("I fucked up, error msg above.")
        time.sleep(60)
        return 1

def gemInfo(gem):
    with open('weightings.json', 'r') as f:
        gemData = json.load(f)
    for active in gemData["active"]:
        if gem == active:
            return [gemData["active"][gem]["weights"], gemData["active"][gem]["images"]["gemIcon"], gem]
    if "Support" not in gem:
        gem = gem + " Support"
    for support in gemData["support"]:
        if gem == support:
            return [gemData["support"][gem]["weights"],gemData["support"][gem]["images"]["gemIcon"], gem]
    print("Error")
    return "Error"

def gemPrice(gem, quality):
    with open('pricejson.json', 'r') as f:
        priceData = json.load(f)
    for active in priceData["active"]:
        if gem == active:
             return priceData["active"][gem][quality]
    if "Support" not in gem:
        gem = gem + " Support"
    for support in priceData["support"]:
        if gem == support:
            return priceData["support"][gem][quality]

def gemProfit(gem):
    with open('profit.json') as f:
        profitData = json.load(f)
    return profitData[gem]


def sleepError(errormsg):
    print(errormsg)
    time.sleep(120)
