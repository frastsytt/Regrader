import urllib.request, json
import requests
from bs4 import BeautifulSoup
import time

req = urllib.request.Request("https://www.pathofexile.com/api/trade/data/items", headers={'User-Agent': 'Mozilla/5.0'})
webpage = json.loads(urllib.request.urlopen(req).read())

data_set = {"active": {}, "support": {}}
weights_dict = data_set
jsonfile = 'weightings.json'

print(data_set)

for value in webpage["result"]:
    if value["id"] == "gems" and value["id"] != None:
        if value["entries"] != None:
            for gem in value["entries"]:
                if "Vaal" not in gem["text"] and "Awakened" not in gem["text"]:
                    if "Support" not in gem["text"]:
                        tempvar = {gem["text"] : {}}
                        data_set["active"].update(tempvar)
                    elif "Support" in gem["text"]:
                        tempvar = {gem["text"]: {}}
                        data_set["support"].update(tempvar)
                    pass
                else:
                    pass
        else:
            pass

gemTotalCount = len(data_set["active"].keys()) + len(data_set["support"].keys())
countPercent = 0
print(gemTotalCount)

url = "https://poedb.tw/us/"
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Regrader/1.0 roomet.sytt@voco.ee guki#7589 https://github.com/frastsytt/Regrader'
    }

for active_support in data_set:
    for querygem in data_set[active_support].keys():
        tempgem = querygem
        querygem = querygem.replace(" ", "_")
        querygem = querygem.replace("\'", "")
        url = f'https://poedb.tw/us/{querygem}'

        emptyDict = {"weights": {},
                     "images": {}}

        weights_dict[active_support][tempgem].update(emptyDict)

        # get response for each gem
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        print(f'Currently getting: {url}')
        skillgem = ""
        if active_support == "active":
            for a in soup.find("ul", {"class": f'nav nav-tabs d-flex flex-wrap'}).find_all('a', href=True):
                if "SkillGem" in str(a):
                    skillgem = a['href'][1:]
                else:
                    pass

        elif active_support == "support":
            for a in soup.find("ul", {"class": f'nav nav-tabs d-flex flex-wrap'}).find_all('a', href=True):
                if "SupportGem" in str(a):
                    skillgem = a['href'][1:]
                else:
                    pass

        for regradevalue in soup.find("div", {"id": f'{skillgem}'}).find("div", {"class": "table-responsive"}).find('tbody').find_all('tr'):
            tempvar = {regradevalue.find('td').text.replace(" ", "") : {"value": int(regradevalue.find_all('td')[2].text),
                                                                        "qualityBonus": str(regradevalue.find_all('td')[1].text)}}
            weights_dict[active_support][tempgem]["weights"].update(tempvar)

        for i, itemBoxImage in enumerate(soup.find_all("div", {"class": "itemboximage"})):
            if i < 1:
                for j, imgDiv in enumerate(itemBoxImage.find_all("img")):
                    if j == 0:
                        tempvar = {"gemIcon": imgDiv['src']}
                        weights_dict[active_support][tempgem]["images"].update(tempvar)
                    elif j == 1:
                        tempvar = {"skillIcon": imgDiv['src']}
                        weights_dict[active_support][tempgem]["images"].update(tempvar)
                    else:
                        pass
            else:
                continue
        print(weights_dict[active_support][tempgem])
        countPercent += 1
        print(f'{round((countPercent / gemTotalCount) * 100)}% done...')
        time.sleep(0.25)


with open(jsonfile, 'w') as outfile:
    json.dump(weights_dict, outfile, indent=4)
