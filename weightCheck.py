import urllib.request, json, requests, statistics
import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def weighting(gem):
    querygem= gem.replace(" ", "_")
    querygem = gem.replace("\'", "")
    url = f'https://poedb.tw/us/{gem}'
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(f'Currently getting :{url}')
    skillgem = ""
    for a in soup.find("ul", {"class": f'nav nav-tabs d-flex flex-wrap'}).find_all('a', href=True):
        if "SkillGem" in str(a) or "SupportGem" in str(a):
            skillgem = a['href'][1:]
        else:
            pass

    #print(soup.find("div", {"id": f'{skillgem}'}))
    response = "```"
    for regradevalue in soup.find("div", {"id": f'{skillgem}'}).find("div", {"class": "table-responsive"}).find('tbody').find_all('tr'):
        response += regradevalue.find('td').text
        response += ": "
        response += regradevalue.find_all('td')[2].text
        response += "\n"
    response += "```"
    return(response)


