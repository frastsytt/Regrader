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
            print(respo["id"] + " - tradelink for: " + gem + altqual)
            count = 0
            insertable = ''

            # build up the string that needs to be in the url
            for item in respo["result"]:
                insertable += item + ','
                count += 1
                if count > 8:
                    break

            fetchurl = 'https://www.pathofexile.com/api/trade/fetch/' + insertable + '?query=' + respo["id"]

            # try to GET a gem trade listings, if it fails it skips the current iteration
            try:
                z = requests.get(fetchurl, headers=headers)
            except Exception as e:
                print(e)
                print("I fucked up, error msg above.")
                continue

            # start calcuating the median price of gem of current iteration
            avgcalc = []

            # only use chaos and ex values, if ex value convert to chaos
            for avg in json.loads(z.text)["result"]:
                if avg is None:
                    break
                elif avg["listing"]["price"]["currency"] == "exalt":
                    avgcalc.append(avg["listing"]["price"]["amount"] * exvalue)
                elif avg["listing"]["price"]["currency"] == "chaos":
                    avgcalc.append(avg["listing"]["price"]["amount"])
                else:
                    pass

            print(f"The average price of {altqual}_{gem} is: {(statistics.median(avgcalc)) - 1}")

            # build small dictionary to be inserted into the big dictionary
            alt_price = {altqual: ((statistics.median(avgcalc)) - 1)}
            data_set[gemtype][gem].update(alt_price)

            # ??? why is this not printing
            print(data_set[gemtype][gem][altqual])

            time.sleep(10)

# set file that the dictionary will be saved to
jsonfile = 'pricejson.json'
with open(jsonfile, 'w') as outfile:
    json.dump(data_set, outfile, indent=4)

# TEST AREA

N = 3
print("The original dictionary is : " + str(data_set))
res = nlargest(N, data_set, key=data_set.get)
print("The top N value pairs are  " + str(res))
