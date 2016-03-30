import json

f = open(r'D:\codehome\flaskkingdom\sheetmod.json' ,'r')
#json.load loads json from file or file like object
#json.loads loads json from a given string or unicode object
json_data = json.load(f)
#parsed = json.load(json_data)
#print json_data['charname']
print json_data