import urllib.request, json, requests, statistics


req = urllib.request.Request("https://www.pathofexile.com/api/trade/data/items", headers={'User-Agent': 'Mozilla/5.0'})
webpage = json.loads(urllib.request.urlopen(req).read())


for value in webpage["result"]:
    if value["id"] == "gems":
        print(value["entries"])

url = 'https://www.pathofexile.com/api/trade/search/Standard'
myobj = {"query":{"status":{"option":"online"},"type":"Enlighten Support","stats":[{"type":"and","filters":[]}]},"sort":{"price":"asc"}}

headers = {'User-Agent': 'Mozilla/5.0', 'content-type': 'application/json'}

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

avgcalc = []

for avg in json.loads(z.text)["result"]:
    if avg == None:
        break
    avgcalc.append(avg["listing"]["price"]["amount"])



print((statistics.median(avgcalc)) - 1)

#https://www.pathofexile.com/api/trade/fetch/RESULT_LINES_HERE?query= + respo["id"]