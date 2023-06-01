# -*- coding: UTF-8 -*-
import sys, os, requests, json, vdf

apikey = sys.argv[1]

defindexes = []
res = requests.get('https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?appid=570&key='+apikey)
res = json.loads(res.text)
for d in res["result"]["assets"]:
	if d["prices"]["USD"] != 0:
		defindexes.append(d["name"])

schema = []
itemsGame = vdf.load(open('items_game.txt', encoding='utf8'), mapper=dict)
items = itemsGame["items_game"]["items"]
for dindex in defindexes:
	if dindex not in items:
		items[dindex] = {
			"name": "#Unknown",
			"item_name": "",
			"item_description": ""
		}
	if "item_description" not in items[dindex]:
		items[dindex]["item_description"] = ""
	item = {
		"name": items[dindex]["name"],
		"defindex": dindex,
		"item_name": items[dindex]["item_name"],
		"item_description": items[dindex]["item_description"]
	}
	schema.append(item)

languageEN = json.load(open('items_english.json', encoding='utf8'))["lang"]["Tokens"]
languageEN = dict((k.lower(), v) for k, v in languageEN.items())
outputEN = {"result": {"items": []}}
for item in schema:
	itemName = languageEN[item["item_name"][1:].lower()] if item["item_name"][1:].lower() in languageEN else item["item_name"]
	itemDesc = languageEN[item["item_description"][1:].lower()] if item["item_description"][1:].lower() in languageEN else item["item_description"]
	if item["name"] == "#Unknown":
		itemName = "Unknown item " + item["defindex"]
		name = item["defindex"]
	else:
		name = item["name"]
	tItem =  {
		"name": name,
		"defindex": item["defindex"],
		"item_name": itemName,
		"item_description": itemDesc
	}
	outputEN["result"]["items"].append(tItem)

languageCN = json.load(open('items_schinese.json', encoding='utf8'))["lang"]["Tokens"]
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
	if item["name"] == "#Unknown":
		itemName = "未知物品 " + item["defindex"]
		name = item["defindex"]
	else:
		item["name"]
	tItem =  {
		"name": name,
		"defindex": item["defindex"],
		"item_name": itemName,
		"item_description": itemDesc
	}
	outputCN["result"]["items"].append(tItem)

with open('schema_en-US.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(outputEN, ensure_ascii=False))
with open('schema_zh-CN.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(outputCN, ensure_ascii=False))
