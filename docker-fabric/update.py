import json
import os
import urllib.request

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

os.system("rm "+ filename)

f = open(filename, "a")

def getversion(url):
    url = urllib.request.urlopen(url)
    data = url.read()
    mydict = json.loads(data)
    return mydict

f.write(str(getversion("https://meta.fabricmc.net/v2/versions/installer")[0]["version"])+"\n")
f.write(str(getversion("https://meta.fabricmc.net/v2/versions/loader/")[0]["version"])+"\n")

mydict = getversion("https://meta.fabricmc.net/v2/versions/")["game"]
stable = {}
lastversion = ""
j=0

for i in range(len(mydict)):

    if mydict[i]["stable"]:

        stable[j] = mydict[i]["version"]
        j=j+1

for i in range(len(stable)):

    if lastversion == "" or lastversion.split(".")[1] != stable[i].split(".")[1]:

        f.write(str(stable[i])+"\n")

    lastversion = stable[i]
f.close()
f=open("versionsandbuilds.txt","r")
d=f.read()
f.close()
m=d.split("\n")
s="\n".join(m[:-1])
f=open("versionsandbuilds.txt","w+")
for i in range(len(s)):
    f.write(s[i])
f.close()

print("Update Complete!")
