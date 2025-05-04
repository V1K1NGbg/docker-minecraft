import json
import os
import urllib.request

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

os.system("rm "+ filename)

f = open(filename, "a")

def getversion(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url = urllib.request.urlopen(req)
    data = url.read()
    mydict = json.loads(data)
    return mydict

j = getversion("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json")

# print(j["promos"]["1.1-latest"])

allov = [x.split("-")[0] for x in j["promos"] if x.split("-")[1] == "recommended"]
allv = j["promos"]

# print(allv)

l = "1."

for i in allov:

    if (''.join(filter(str.isdigit, i.split(".")[1])) != ''.join(filter(str.isdigit, l.split(".")[1]))) and int(''.join(filter(str.isdigit, i.split(".")[1]))) > 7:
        
        f.write(l+"\n")
        f.write(allv[l + "-recommended"]+"\n")

        if int(l.split(".")[1]) >= 20:
            f.write("21\n")
        elif int(l.split(".")[1]) >= 17:
            f.write("17\n")
        elif int(l.split(".")[1]) >= 13:
            f.write("11\n")
        else:
            f.write("8\n")

    l = i

f.write(l+"\n")
f.write(allv[l + "-recommended"]+"\n")
f.write("21")

f.close()

print("Update Complete!")
