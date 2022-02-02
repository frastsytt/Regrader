import urllib.request, json, requests, statistics, time
from heapq import nlargest

# get all gems
req = urllib.request.Request("https://www.pathofexile.com/api/trade/data/items", headers={'User-Agent': 'Mozilla/5.0'})
webpage = json.loads(urllib.request.urlopen(req).read())

# temp orb prices
exvalue = 120
primary = 50
secondary = 80

# read weightings.json so that we can query all alt gem types
with open('weightings.json') as f:
    data = json.load(f)

# need this dictionary for myobj query
query_dict = {"Superior": "0",
              "Anomalous": "1",
              "Divergent": "2",
              "Phantasmal": "3"}

# static urls + headers
url = 'https://www.pathofexile.com/api/trade/search/Standard'
headers = {'User-Agent': 'Mozilla/5.0', 'content-type': 'application/json'}

# start making the pricejson dictionary
data_set = {"active": {}, "support": {}}

for value in webpage["result"]:
    if value["id"] == "gems" and value["id"] is not None:
        if value["entries"] is not None:
            for gem in value["entries"]:
                if "Vaal" not in gem["text"] and "Awakened" not in gem["text"]:
                    if "Support" not in gem["text"]:
                        tempvar = {gem["text"]: {}}
                        data_set["active"].update(tempvar)
                    elif "Support" in gem["text"]:
                        tempvar = {gem["text"]: {}}
                        data_set["support"].update(tempvar)
                    pass
                else:
                    pass
        else:
            pass

# start putting prices into pricejson
for gemtype in data:
    for gem in data[gemtype]:
        for altqual in data[gemtype][gem].keys():
            # build up the post message to get trade listings
            myobj = {"query": {"status": {"option": "online"}, "type": gem,
                               "stats": [{"type": "and", "filters": [], "disabled": False}], "filters": {
                    "misc_filters": {"filters": {"gem_alternate_quality": {"option": query_dict[altqual]}},
                                     "disabled": False}}}, "sort": {"price": "asc"}}
            obj_post = requests.post(url, data=json.dumps(myobj), headers=headers)
            respo = json.loads(obj_post.text)
            print(respo["id"] + " - tradelink for: " + altqual + gem)
            count = 0
            insertable = ''

            # build up the string that needs to be in the url
            for item in respo["result"]:
                insertable += item + ','
                count += 1
                if count > 8:
                    break

            fetchurl = 'https://www.pathofexile.com/api/trade/fetch/' + insertable + '?query=' + respo["id"]

            # try to GET gem trade listings, if it fails it skips the current iteration
            avgcalc = []
            try:
                z = requests.get(fetchurl, headers=headers)
                time.sleep(0.1)
                for avg in json.loads(z.text)["result"]:
                    if avg is None:
                        break
                    elif avg["listing"]["price"]["currency"] == "exalted":
                        avgcalc.append(avg["listing"]["price"]["amount"] * exvalue)
                    elif avg["listing"]["price"]["currency"] == "chaos":
                        avgcalc.append(avg["listing"]["price"]["amount"])
                    else:
                        avgcalc.append(1)
                        pass

                print(f"The average price of {altqual}_{gem} is: {(statistics.median(avgcalc)) - 1}")

                # build small dictionary to be inserted into the big dictionary
                alt_price = {altqual: ((statistics.median(avgcalc)) - 1)}
                data_set[gemtype][gem].update(alt_price)

                # ??? why is this not printing
                print(data_set[gemtype][gem])
                print(data_set[gemtype][gem][altqual])
            except Exception as e:
                print(e)
                print(z.text)
                print("I fucked up, error msg above.")
                time.sleep(60)
                continue

            time.sleep(2.1)

# set file that the dictionary will be saved to
jsonfile = 'pricejson.json'
with open(jsonfile, 'w') as outfile:
    json.dump(data_set, outfile, indent=4)

# TEST AREA

expectedreturn = {}

for gemtype in data:
    for gem in data[gemtype]:
        weightsum = 0
        exppreturn = 0
        for altqual in data[gemtype][gem][altqual[1:]].keys():
            if altqual == "Superior":
                continue
            else:
                weightsum += data[gemtype][gem][altqual].values()
        for _altqual in data[gemtype][gem][altqual[1:]].keys():
            exppreturn += data[gemtype][gem][_altqual] * data_set[gemtype][gem][_altqual]

        if gemtype == "active":
            print(f"{exppreturn - primary} - expected return of using primary lens on {gem}")
        elif gemtype == "support":
            print(f"{exppreturn - secondary} - expected return of using secondary lens on {gem}")
        else:
            pass

        temp = {gem : exppreturn}
        expectedreturn.update(temp)



N = 10
print("The original dictionary is : " + str(expectedreturn))
res = nlargest(N, expectedreturn, key=expectedreturn.get)
print("The top N value pairs are  " + str(res))
