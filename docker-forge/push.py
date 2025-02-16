import os

versions = {}
versionsshort = {}
builds = {}
long_file = {}
loc = {}
count = 0
number = 0

os.system("python3 update.py")

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

f = open(filename)

lines = len(f.readlines())
f.seek(0)

while count < lines:

    # print(number, count, versions, versionsshort, builds)

    if count % 2 == 0:

        versions[number] = f.readline().replace('\n', '')
        versionsshort[number] = versions[number].split('.')[0] + "." + versions[number].split('.')[1]
        if int(versionsshort[number].split(".")[1]) < 10:

            long_file[number] = "-"+versions[number]

        else:

            long_file[number] = ""

        if int(versionsshort[number].split(".")[1]) < 17:

            loc[number] = "older/."

        # elif int(versionsshort[number].split(".")[1]) < 20:

        #     loc[number] = "old/."

        else:

            loc[number] = "."

    else:

        builds[number] = f.readline().replace('\n', '')
        number = number + 1

    count = count + 1

os.system('docker container prune -f')
os.system('docker image prune -f')

for x in range(0, round(lines/2)):

    os.system("docker image rm v1k1ngbg/forge:"+versionsshort[x]+" -f")
    os.system("docker build -t v1k1ngbg/forge:"+versionsshort[x]+" --build-arg version="+versions[x]+" --build-arg build="+builds[x]+" --build-arg long_file="+long_file[x]+" "+loc[x])
    os.system("docker push v1k1ngbg/forge:"+versionsshort[x])

os.system('docker image prune -f')

f.close()
