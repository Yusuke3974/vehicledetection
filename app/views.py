from app import app
from flask import request, render_template,url_for
import cv2
import numpy as np
from PIL import Image
import string
import random
import os

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

car_cascade_src = 'app/static/cascade/cars.xml'
bus_cascade_src = 'app/static/cascade/Bus_front.xml'


@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'GET':
        full_filename = 'images/white_bg.jpg'
        return render_template('index.html', full_filename = full_filename)

    if request.method == 'POST':

        image_upload = request.files['image_upload']
        imagename = image_upload.filename

        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10) + '.jpg')
        full_filename = 'uploads/' + name

        image = Image.open(image_upload)
        image = image.resize((450,250))
        image_arr = np.array(image)
        grey = cv2.cvtColor(image_arr,cv2.COLOR_BGR2GRAY)
        
        #車用のカスケードファイル
        car_cascade = cv2.CascadeClassifier(car_cascade_src)
        cars = car_cascade.detectMultiScale(grey,1.1,1)

        #バス用のカスケードファイル
        bcnt = 0
        bus_cascade = cv2.CascadeClassifier(bus_cascade_src)
        bus = bus_cascade.detectMultiScale(grey,1.1,1)

        for (x,y,w,h) in bus:
            cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
            bcnt += 1

        ccnt = 0
        for (x,y,w,h) in cars:
            cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
            ccnt += 1

        img = Image.fromarray(image_arr,'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
        result = str(ccnt) + "：車の数" + str(bcnt) + '：バスの数'
        return render_template('index.html',full_filename=full_filename,pred=result)

if __name__ == '__main__':
    app.run(debug=True)