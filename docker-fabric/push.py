import os

version = {}
versionshort = {}
loader = ""
installer = ""
count = 0

os.system('python3 update.py')

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

f = open(filename)

lines = len(f.readlines())
f.seek(0)

installer = f.readline().replace('\n', '')
loader = f.readline().replace('\n', '')

while count < lines-2:

    """print(count, installer, loader, version, versionshort)"""
    version[count] = f.readline().replace('\n', '')
    versionshort[count] = version[count].split('.')[0] + "." + version[count].split('.')[1]
    count = count + 1

os.system('docker container prune -f')
os.system('docker image prune -f')

for x in range(0, round(lines-2)):

    os.system("docker image rm v1k1ngbg/fabric:"+versionshort[x]+" -f")
    os.system("docker build -t v1k1ngbg/fabric:"+versionshort[x]+" --build-arg version="+version[x]+" --build-arg loader="+loader+" --build-arg installer="+installer+" .")
    os.system("docker push v1k1ngbg/fabric:"+versionshort[x])

os.system('docker image prune -f')

f.close()
