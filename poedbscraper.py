import urllib.request, json, requests, statistics
import requests
from bs4 import BeautifulSoup
import re
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

url = "https://poedb.tw/us/"
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


for querygem in data_set["active"].keys():
    tempgem = querygem
    prefixing = querygem.replace(" ", "")
    prefixing = querygem.replace("\'", "")
    querygem = querygem.replace(" ", "_")
    querygem = querygem.replace("\'", "")
    url = f'https://poedb.tw/us/{querygem}'

    # get response for each gem
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'Currently getting: {url}')
    skillgem = ""
    for a in soup.find("ul", {"class": f'nav nav-tabs d-flex flex-wrap'}).find_all('a', href=True):
        if "SkillGem" in str(a):
            skillgem = a['href'][1:]
        else:
            pass

    for regradevalue in soup.find("div", {"id": f'{skillgem}'}).find("div", {"class": "table-responsive"}).find('tbody').find_all('tr'):
        tempvar = {regradevalue.find('td').text.replace(" ", "") : regradevalue.find_all('td')[2].text}
        weights_dict["active"][tempgem].update(tempvar)
    time.sleep(0.25)


for querygem in data_set["support"].keys():
    tempgem = querygem
    prefixing = querygem.replace(" ", "")
    prefixing = querygem.replace("\'", "")
    querygem = querygem.replace(" ", "_")
    querygem = querygem.replace("\'", "")
    url = f'https://poedb.tw/us/{querygem}'

    # get response for each gem
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'Currently getting: {url}')
    skillgem = ""
    for a in soup.find("ul", {"class": f'nav nav-tabs d-flex flex-wrap'}).find_all('a', href=True):
        if "SupportGem" in str(a):
            skillgem = a['href'][1:]
        else:
            pass

    for regradevalue in soup.find("div", {"id": f'{skillgem}'}).find("div", {"class": "table-responsive"}).find('tbody').find_all('tr'):
        tempvar = {regradevalue.find('td').text.replace(" ", "") : regradevalue.find_all('td')[2].text}
        weights_dict["support"][tempgem].update(tempvar)
    time.sleep(0.25)


with open(jsonfile, 'w') as outfile:
    json.dump(weights_dict, outfile, indent=4)
