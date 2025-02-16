import os

count = 0
number = 0

os.system("python3 update.py")

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'versionsandbuilds.txt')

f = open(filename)

version = f.readline().replace('\n', '')
build = f.readline().replace('\n', '')

os.system('docker container prune -f')
os.system('docker image prune -f')

os.system("docker image rm v1k1ngbg/velocity:"+version.split(".")[0]+" -f")
os.system("docker build -t v1k1ngbg/velocity:"+version.split(".")[0]+" --build-arg version="+version+" --build-arg build="+build+" .")
os.system("docker push v1k1ngbg/velocity:"+version.split(".")[0])

version = f.readline().replace('\n', '')
build = f.readline().replace('\n', '')

os.system("docker image rm v1k1ngbg/velocity:"+version.split(".")[0]+"S -f")
os.system("docker build -t v1k1ngbg/velocity:"+version.split(".")[0]+"S --build-arg version="+version+" --build-arg build="+build+" .")
os.system("docker push v1k1ngbg/velocity:"+version.split(".")[0]+"S")

os.system('docker image prune -f')

f.close()
