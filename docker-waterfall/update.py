import json
import os
import urllib.request

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

os.system("rm "+filename)

f = open(filename, "a")

def readandprocess(url):
    url = urllib.request.urlopen(url)
    data = url.read()
    mydict = json.loads(data)
    return mydict

mydict = readandprocess("https://api.papermc.io/v2/projects/waterfall/")
lastversion = ""

for i in range(len(mydict["versions"])):

    if lastversion != "" and lastversion.split(".")[1] != mydict["versions"][i].split(".")[1] and lastversion!="1.13-pre7":

        f.write(str(lastversion)+"\n")
        f.write(str(readandprocess("https://api.papermc.io/v2/projects/waterfall/versions/"+lastversion)["builds"][-1])+"\n")

    lastversion = mydict["versions"][i]

f.write(str(mydict["versions"][i])+"\n")
f.write(str(readandprocess("https://api.papermc.io/v2/projects/waterfall/versions/"+mydict["versions"][i])["builds"][-1]))

f.close()

print("Update Complete!")
