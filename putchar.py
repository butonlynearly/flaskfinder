import os, json
import requests

with open(r'D:\codehome\flaskkingdom\sheetmod.json') as json_data:
	d = json.load(json_data)
	json_data.close()
	
print d



r = requests.put('http://127.0.0.1:3000/character', data = d)	
