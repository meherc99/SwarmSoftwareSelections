from flask import Flask, jsonify, abort, request, make_response, url_for,redirect,send_file
import sys
import numpy as np
from PIL import Image
import random
import time

img=None
botPose=[[0,0]]
obstaclePose=[]
app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found1(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found2(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/', methods = ['GET'])
def getInfo():
    return redirect('/map')
    
@app.route('/map', methods = ['GET'])   #Hosts map at http://127.0.0.1:5000/map
def getMap():
    return send_file('images/map.png', mimetype='image/png',cache_timeout=-1)

@app.route('/botPose', methods = ['GET']) #Hosts botPose at http://127.0.0.1:5000/botPose and so on
def getBotPose():
    global botPose
    return jsonify(botPose)

@app.route('/obstaclesPose', methods = ['GET'])
def getObstaclePose():
    global obstaclePose
    return jsonify(obstaclePose)

@app.route('/finalPose', methods = ['GET'])
def getFinalPose():
    global img
    return jsonify([img.shape[0]-1,img.shape[0]-1])

@app.route('/move', methods = ['GET'])
def move():
    global botPose,obstaclePose
    data=request.json
    if 'botId' not in data or 'moveType' not in data:
        abort(400)
    data['botId']=int(data['botId'])
    data['moveType']=int(data['moveType'])
    if data['botId']<=0 or data['botId']>len(botPose):
        abort(400)
    if data['moveType']<=0 or data['moveType']>8:
        abort(400)
    pass    
    return jsonify({'success': 0})

def createImage(size1,size2):
    global img,obstaclePose
    size=size2//2
    arr=[[0,0],[0,1],[1,0],[1,1]]
    random.seed(time.time())
    img=np.ones((size1,size1,3),dtype=np.uint8)*255
    xTop=0
    while xTop<size1:
        yTop=0
        while yTop<size1:
            num=random.randint(0,3)
            newX=xTop+arr[num][0]*(size2//2)
            newY=yTop+arr[num][1]*(size2//2)
            if (newX==0 and newY==0) or (newX==size1-(size2//2) and newY==size1-(size2//2)):
                pass
            else:
                img[newX:newX+(size2//2),newY:newY+(size2//2),:]=np.zeros((size2//2,size2//2,3))
                obstaclePose.append([[newX,newY],[newX,newY+size],[newX+size,newY+size],[newX+size,newY]])
            yTop=yTop+size2
        xTop=xTop+size2
    im=Image.fromarray(img)
    im.save("images/map.png")

createImage(200,40)

if  __name__=="__main__":
    app.run(debug = True)