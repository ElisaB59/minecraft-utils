import json
from collections import Counter
import decimal

ctx = decimal.Context()
def float_to_str(f):
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

filename = input("Enter file path: ")
f = open(filename)
data = json.load(f)
f.close
finalData = []

for item in data:
    block = item["block"].replace(":", ":deepslate_")
    distrib = Counter({i.split(",")[0]: float(i.split(",")[1]) for i in item["distrib"][:-1].split(";")})
    dim = item["dim"]
    deepOre = [ore1 for ore1 in data if (ore1["dim"] == dim
									  and ore1["block"] == block)]
    if len(deepOre) > 0 :
        deepOre = deepOre[0]
        deepDistrib = Counter({i.split(",")[0]: float(i.split(",")[1]) for i in deepOre["distrib"][:-1].split(";")})
        dictArray = [distrib, deepDistrib]
        realDistrib = distrib + deepDistrib
        distrib.update(realDistrib)
        finalDistrib = ';'.join([key+","+float_to_str(value) for key, value in distrib.items()])
        item["distrib"] =  finalDistrib
        deepOre["distrib"] = finalDistrib	
    if "ore" in item["block"]:
        finalData.append(item)


with open(filename+".merged", 'w') as f:
    json.dump(finalData, f, indent=4), 