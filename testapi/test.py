import postdata
import base64
from datetime import datetime
import json
import cv2


def convert_imgarr2base64(img_arr):
    """
    Convert numpy array image to string base64
    Parameters:
        -img_arr: array of image.
    """
    try:
        _, img_encoded = cv2.imencode('.jpg', img_arr)
        jpg_as_text = base64.b64encode(img_encoded).decode('utf-8')
        return jpg_as_text
    except:
        return None


now = datetime.now()


def Time(hour):
    return now.replace(hour=hour, minute=0, second=0, microsecond=0)


def to_shift(time):
    """
    Convert day to shift
    -1 is outside of school hours
    """
    if Time(7) <= time < Time(9):
        return 1
    if Time(9) <= time < Time(11):
        return 2
    if Time(12) <= time < Time(14):
        return 3
    if Time(14) <= time < Time(16):
        return 4
    if Time(16) <= time < Time(18):
        return 5
    if Time(18) <= time < Time(20):
        return 6
    else:
        return -1


def up_data(id_cam, img, label):
    '''
        image: str, label: int, id_cam: int, time, shift: int
    '''
    url = ""
    data = {"id_cam": id_cam, "label": label}
    base64img = convert_imgarr2base64(img)
    json_data = None
    if base64img is not None:
        data["image"] = base64img
        data["time"] = datetime.now()
        data["shift"] = to_shift(datetime.now())
        response = postdata.post(url, json=data)
        json_data = json.loads(response.txt)
    return json_data
