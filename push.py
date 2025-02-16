import os

os.system('docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)')

os.system('cd docker-paper && python3 push.py && cd ..')
os.system('cd docker-fabric && python3 push.py && cd ..')
os.system('cd docker-forge && python3 push.py && cd ..')
os.system('cd docker-velocity && python3 push.py && cd ..')
os.system('cd docker-vanilla && python3 push.py && cd ..')
# os.system('cd docker-waterfall && python3 push.py && cd ..')

os.system('cd Discord-bot && docker build -t v1k1ngbg/discord-bot ./Discord-bot/ && docker push v1k1ngbg/discord-bot && cd ..')
os.system('docker run -d --restart=always -v ~/server/config.json:/usr/bot/config/config.json -v /var/run/docker.sock:/var/run/docker.sock --name discord-bot v1k1ngbg/discord-bot:latest')
