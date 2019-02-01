import requests

#testing move api

url = 'http://127.0.0.1:5000/move'

command = {
            'botId': 2,
            'moveType':4
}

r=requests.get(url,json=command)

print(r.json()['success'])

#testing obstaclesPose api

url = 'http://127.0.0.1:5000/obstaclesPose'

r=requests.get(url)

print(r.json()[1]['posX'])  #getting x-co-ordinate of 2nd obstacle

url = 'http://127.0.0.1:5000/botPose'

r=requests.get(url)

print(r.json()[1]['posX'])  #getting x-co-ordinate of 2nd bot