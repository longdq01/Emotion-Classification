import cv2
import numpy as np
from cv2 import dnn
from numpy.lib.type_check import imag
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.python.framework.ops import device
from ultra_face_opencvdnn_inference import Light_Face
import tensorflow as tf
from post import up_data
import base64
from datetime import datetime

def real_time_AI():
    model=tf.keras.models.load_model(r'/home/long/Desktop/feel_project-main/model100_mobilenetv3_final1.h5') # model h5
    detector=Light_Face(r'slim-320.prototxt',r'slim-320.caffemodel') #model detection

    id_cam=0
    device="Web_cam_0"
    cap = cv2.VideoCapture(id_cam)
    while True:
        faces= []
        ret,frame=cap.read()
        boxes=detector.predict_face(frame)

        if boxes is not None:
            # print(boxes)
            for (x,y,w,h) in boxes:
                cv2.rectangle(frame, (x+10,y+5), (w+10,h+5), (255,0,0), 2)
                face=frame[y+5:h+5, x+15:w+10]
                face = cv2.resize(face,(224,224))
                face2 = img_to_array(face)
                face2 = np.expand_dims(face2,axis=0)

                # faces.append(face2)
                label=None
                pred = model.predict(face2)
                idx_max = np.argmax(pred[0])
                class_names = ['Angry','Fear','Happy','Neutral','Sad','Surprise']
                cv2.putText(frame, class_names[idx_max], (x+5, y-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                label=class_names[idx_max]
                # if label is not None:
                    # schedule.every(10).minutes.do(up_data(id_cam,face2,label,device))
                print(label)

                data = up_data(5,face,label)
                print(data)

                # filename = str(datetime.now())+'.jpg'
                # with open(filename,"wb") as f:
                #     f.write(base64.b64decode(data['image'].encode('utf-8')))

            cv2.imshow('Box',frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

real_time_AI()
