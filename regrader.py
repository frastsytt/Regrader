import urllib.request, json, requests, statistics, itertools, time


req = urllib.request.Request("https://www.pathofexile.com/api/trade/data/items", headers={'User-Agent': 'Mozilla/5.0'})
webpage = json.loads(urllib.request.urlopen(req).read())

exvalue = 120

for value in webpage["result"]:
    if value["id"] == "gems":
        print(value["entries"])

with open('weightings.json') as f:
   data = json.load(f)

#print(data)

query_dict = {"Superior": "0",
              "Anomalous": "1",
              "Divergent": "2",
              "Phantasmal": "3"}

#print(query_dict["Superior"])

url = 'https://www.pathofexile.com/api/trade/search/Standard'
headers = {'User-Agent': 'Mozilla/5.0', 'content-type': 'application/json'}

for gemtype in data:
    for gem in data[gemtype]:
        for altqual in data[gemtype][gem].keys():
            #print(altqual[:-1])
            #print(data[gemtype][gem][altqual])
            #print(query_dict[altqual[:-1]])
            myobj = {"query":{"status":{"option":"online"},"type":gem,"stats":[{"type":"and","filters":[],"disabled":False}],"filters":{"misc_filters":{"filters":{"gem_alternate_quality":{"option":query_dict[altqual[:-1]]}},"disabled":False}}},"sort":{"price":"asc"}}
            #print(myobj)
            x = requests.post(url, data=json.dumps(myobj), headers=headers)
            respo = json.loads(x.text)
            print(respo)
            # for e in respo["result"][0:8]:
            #     print(e)

            count = 0
            insertable = ''

            for item in respo["result"]:
                insertable += item + ','
                count += 1
                if count > 8:
                    break

            fetchurl = 'https://www.pathofexile.com/api/trade/fetch/' + insertable + '?query=' + respo["id"]

            z = requests.get(fetchurl, headers=headers)

            #print(z.text)

            avgcalc = []

            for avg in json.loads(z.text)["result"]:
                if avg == None:
                    break
                elif avg["listing"]["price"]["currency"] == "exalt":
                    avgcalc.append(avg["listing"]["price"]["amount"] * exvalue)
                elif avg["listing"]["price"]["currency"] == "chaos":
                    avgcalc.append(avg["listing"]["price"]["amount"])
                else:
                    pass
            #print(avgcalc)
            print(f"The average price of {altqual}{gem} is: ")
            print((statistics.median(avgcalc)) - 1)

            time.sleep(10)



x = requests.post(url, data=json.dumps(myobj), headers=headers)

print(x.json())

respo = json.loads(x.text)


for e in respo["result"][0:8]:
    print(e)

count = 0
insertable = ''

for item in respo["result"]:
    insertable += item + ','
    count += 1
    if count > 8:
        break


fetchurl = 'https://www.pathofexile.com/api/trade/fetch/' + insertable + '?query=' + respo["id"]

z = requests.get(fetchurl, headers=headers)

print(z.text)

avgcalc = []

for avg in json.loads(z.text)["result"]:
    if avg == None:
        break
    avgcalc.append(avg["listing"]["price"]["amount"])



print((statistics.median(avgcalc)) - 1)

#https://www.pathofexile.com/api/trade/fetch/RESULT_LINES_HERE?query= + respo["id"]