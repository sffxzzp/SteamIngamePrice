# -*- coding: utf-8 -*-
import requests, json

apikey = 'apikey here'

res = requests.get('https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?language=zh-CN&appid=730&key='+apikey, verify=False)
pricedata = res.json()
defindexes = []
for item in pricedata['result']['assets']:
	defindexes.append(int(item['name']))

res = requests.get('https://api.steampowered.com/IEconItems_730/GetSchema/v2/?language=zh-CN&key='+apikey, verify=False)
schemadata = res.json()
items = []
for item in schemadata['result']['items']:
	if item['defindex'] in defindexes:
		items.append(item)
outdata = {
	'result': {
		'items': items
	}
}
with open('schema.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(outdata, ensure_ascii=False))