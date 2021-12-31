from flask import Flask, redirect, url_for, render_template, session, request, flash, jsonify
from datetime import timedelta, datetime, date
from database.User import User
from database.sql import SQL_Server
import os
import base64
# from flask_ngrok import run_with_ngrok


app = Flask(__name__)
# run_with_ngrok(app)
sql = SQL_Server()

app.secret_key = 'mykey'
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        password = request.form['pass']

        if User.find_user(user, password):
            session['user'] = user
            session['password'] = password
            return redirect(url_for('home'))
        else:
            flash('Không tìm thấy tài khoản hoặc mật khẩu trùng')
            return render_template('login.html')
    else:
        if 'user' in session and 'password' in session:
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/home')
def home():
    if 'user' in session and 'password' in session:
        # get list camera
        query = 'SELECT * FROM dbo.Camera'
        listCamera = sql.select(query)

        # get infor of camera includes:  use smartphone, use laptop,  others...
        thietbi = listCamera[0][0]
        query1 = "select COUNT(*) FROM dbo.Emotion where LoaiCamXuc =6 and Kip=1 and ThietBi ={} and CONVERT(DATE,Ngay)='{}'".format(
            thietbi, datetime.now())
        query2 = "select COUNT(*) FROM dbo.Emotion where LoaiCamXuc =7 and Kip=1 and ThietBi ={} and CONVERT(DATE,Ngay)='{}'".format(
            thietbi, datetime.now())
        query3 = "select COUNT(*) FROM dbo.Emotion where LoaiCamXuc =8 and Kip=1 and ThietBi ={} and CONVERT(DATE,Ngay)='{}'".format(
            thietbi, datetime.now())
        infor_class = {"useSmartPhone": sql.select(
            query1)[0][0], "useLaptop": sql.select(query2)[0][0]}
        infor_class['other'] = sql.select(query3)[0][0]

        # get infor of chart (list statis about emotion)

        query = "SELECT LoaiCamXuc, COUNT(*) AS SoLuong FROM dbo.Emotion"
        query += " where ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
            thietbi, datetime.now(), 1)
        query += " GROUP BY LoaiCamXuc"

        listEmotion = sql.select(query)
        print(listEmotion)

        data1 = [0, 0, 0, 0, 0, 0]
        label2 = [6, 7, 8]
        for obj in listEmotion:
            if obj[0] not in label2:
                data1[obj[0]] = obj[1]
        print(data1)

        # get list image of first emotion
        query = "SELECT image FROM dbo.Emotion where"
        query += " LoaiCamXuc={} and ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
            0, thietbi, datetime.now(), 1)

        listImage = sql.select(query)

        return render_template('home.html', listCamera=listCamera, infor_class=infor_class,
                               data1=data1, listImage=listImage)
    else:
        return redirect(url_for('index'))


@app.route('/info', methods=['POST'])
def get_emotions_with_camera():
    if request.method == 'POST':
        try:
            data = request.get_json()
            id_cam = data['cameraId']
            date = data['date']
            shift = data['shift']
            e = int(data['emotion'][1])

            query = "SELECT LoaiCamXuc, COUNT(*) AS SoLuong FROM dbo.Emotion"
            query += " where ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
                id_cam, date, shift)
            query += " GROUP BY LoaiCamXuc"

            listEmotion = sql.select(query)
            data = {}
            for emotion in listEmotion:
                data[str(emotion[0])] = emotion[1]

            query = "SELECT image FROM dbo.Emotion where"
            query += " LoaiCamXuc = {} and ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
                e, id_cam, date, shift)

            listImage = sql.select(query)

            data['image'] = [img[0] for img in listImage]
            print(data)
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({'Status': 'Failed', 'msg': str(e)})


@app.route('/post', methods=["POST"])
def insert_data_to_db():
    if request.method == 'POST':
        try:
            data = request.get_json()
            id_cam = data['id_cam']
            # Angry:0,Fear:1,Happy:2,Neutral:3,Sad:4:Surprise:5
            label = data['label']
            image = data['image']  # base64 (string)
            shift = data['shift']
            time = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0)

            emotion_dictionary = {'angry': 0, 'fear': 1,
                                  'happy': 2, 'neutral': 3, 'sad': 4, 'surprise': 5}
            label = emotion_dictionary[label.lower()]

            directory = str(date.today())
            # Parent Directory path
            parent_dir = os.getcwd()
            # Path
            path = parent_dir+"\\"+"static"+"\\"+"image"+"\\"+directory
            try:
                os.mkdir(path)
            except:
                print('Folder exist!')

            # Process base64 string
            filename = str(datetime.now())
            specialChars = "!#$%^&*():.- "
            for specialChar in specialChars:
                filename = filename.replace(specialChar, '')

            url_save_to_db = "static\\image\\"+directory+"\\"+filename+".jpg"
            url_img = path+"\\"+filename
            url_img += '.jpg'
            with open(url_img, "wb") as f:
                f.write(base64.b64decode(image.encode('utf-8')))

            query = "INSERT INTO dbo.Emotion Values ('{}', '{}', '{}', '{}', '{}' )".format(url_save_to_db,
                                                                                            label, id_cam, time, shift)
            sql.insert(query)

            return jsonify({'id_cam': id_cam, 'label': label, 'image': url_img, 'time': time, 'shift': shift})
        except Exception as e:
            print(e)
            return jsonify({'Status': 'Failed', 'msg': str(e)})


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9999')
    # app.run()
