# -*- coding: UTF-8 -*-
import sys, os, requests, json
sys.path.append(os.getcwd())
import vdf

apikey = 'API Key Here.'

defindexes = []
res = requests.get('https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?appid=730&key='+apikey, verify=False)
res = json.loads(res.text)
for d in res["result"]["assets"]:
	defindexes.append(d["name"])

schema = []
itemsGame = vdf.load(open('items_game.txt'), mapper=dict)
items = itemsGame["items_game"]["items"]
for dindex in defindexes:
	if dindex == "1203":
		items[dindex]["item_name"] = "#CSGO_base_crate_key"
		items[dindex]["item_description"] = "#CSGO_base_crate_key_desc"
	item = {
		"name": items[dindex]["name"],
		"defindex": dindex,
		"item_name": items[dindex]["item_name"],
		"item_description": items[dindex]["item_description"],
		# todo: https://github.com/Step7750/node-csgo-cdn
		"image_url": "",
	}
	schema.append(item)

languageEN = vdf.load(open('csgo_english.txt', encoding='utf8'), mapper=dict)["lang"]["Tokens"]
languageEN = dict((k.lower(), v) for k, v in languageEN.items())
outputEN = {"result": {"items": []}}
for item in schema:
	itemName = languageEN[item["item_name"][1:].lower()] if item["item_name"][1:].lower() in languageEN else item["item_name"]
	itemDesc = languageEN[item["item_description"][1:].lower()] if item["item_description"][1:].lower() in languageEN else item["item_description"]
	tItem =  {
		"name": item["name"],
		"defindex": item["defindex"],
		"item_name": itemName,
		"item_description": itemDesc,
		"image_url": "",
	}
	outputEN["result"]["items"].append(tItem)

languageCN = vdf.load(open('csgo_schinese.txt', encoding='utf8'), mapper=dict)["lang"]["Tokens"]
languageCN = dict((k.lower(), v) for k, v in languageCN.items())
outputCN = {"result": {"items": []}}
for item in schema:
	if item["item_name"][1:].lower() in languageCN:
		itemName = languageCN[item["item_name"][1:].lower()]
	elif item["item_name"][1:].lower() in languageEN:
		itemName = languageEN[item["item_name"][1:].lower()]
	else:
		itemName = item["item_name"]
	if item["item_description"][1:].lower() in languageCN:
		itemDesc = languageCN[item["item_description"][1:].lower()]
	elif item["item_description"][1:].lower() in languageEN:
		itemDesc = languageEN[item["item_description"][1:].lower()]
	else:
		itemDesc = item["item_description"]
	tItem =  {
		"name": item["name"],
		"defindex": item["defindex"],
		"item_name": itemName,
		"item_description": itemDesc,
		"image_url": "",
	}
	outputCN["result"]["items"].append(tItem)

with open('schema_en-US.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(outputEN, ensure_ascii=False))
with open('schema_zh-CN.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(outputCN, ensure_ascii=False))