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

j = readandprocess("https://api.papermc.io/v2/projects/velocity/")

mydictns = [x for x in j["versions"] if  not x.endswith("SNAPSHOT")]
mydict = j["versions"]

f.write(str(mydictns[-1])+"\n")
f.write(str(readandprocess("https://api.papermc.io/v2/projects/velocity/versions/"+mydictns[-1])["builds"][-1])+"\n")

f.write(str(mydict[-1])+"\n")
f.write(str(readandprocess("https://api.papermc.io/v2/projects/velocity/versions/"+mydict[-1])["builds"][-1])+"\n")


f.close()

print("Update Complete!")
