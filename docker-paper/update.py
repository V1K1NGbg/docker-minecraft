import json
import os
import urllib.request

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

os.system("rm "+ filename)

f = open(filename, "a")

def readandprocess(url):
    url = urllib.request.urlopen(url)
    data = url.read()
    mydict = json.loads(data)
    return mydict

mydict = readandprocess("https://api.papermc.io/v2/projects/paper/")
lastversion = ""

for i in range(len(mydict["versions"])):

    if lastversion != "" and lastversion.split(".")[1] != mydict["versions"][i].split(".")[1] and lastversion!="1.13-pre7":

        f.write(str(lastversion)+"\n")
        f.write(str(readandprocess("https://api.papermc.io/v2/projects/paper/versions/"+lastversion)["builds"][-1])+"\n")
        
        if int(lastversion.split(".")[1]) >= 20:
            f.write("21\n")
        elif int(lastversion.split(".")[1]) >= 17:
            f.write("17\n")
        elif int(lastversion.split(".")[1]) >= 13:
            f.write("11\n")
        else:
            f.write("8\n")

    lastversion = mydict["versions"][i]

f.write(str(mydict["versions"][i])+"\n")
f.write(str(readandprocess("https://api.papermc.io/v2/projects/paper/versions/"+mydict["versions"][i])["builds"][-1])+"\n")
f.write("21")

f.close()

print("Update Complete!")
