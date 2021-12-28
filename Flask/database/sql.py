import pyodbc
from datetime import datetime
import random


class SQL_Server:

    def __init__(self):
        server = 'DESKTOP-8TG1B6T\SQLEXPRESS'
        database = 'emotionDB'
        username = 'sa'
        password = 'long2001'
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                   server+';DATABASE='+database+';Trusted_Connection=yes;UID='+username+';PWD=' + password)

    def insert(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)
        self.cnxn.commit()

    def select(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)
        data = []
        for row in cursor:
            data.append(row)
        return data


if __name__ == "__main__":

    query = 'SELECT * FROM dbo.Emotion '
   # query2 = "INSERT INTO dbo.DienThoai (MaDienThoai,TenDienThoai,MaHang ,DonGia,SoLuongConLai) VALUES ('DT000045', 'iphone 15', 'HANG002', 1000000, 100)"

    sql = SQL_Server()
    # sql.insert(query2)
    # cursor = sql.select(query)

    # for row in cursor:
    #     row_to_list = [elem for elem in row]
    #     print(row)
    # print(type(cursor), type(cursor[0]))
    # print(list(cursor[0])[0])
    # print(len(cursor))

    # query = "SELECT LoaiCamXuc, COUNT(*) AS SoLuong FROM dbo.Emotion"
    # query += " where ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
    #     3, datetime.now(), 1)
    # query += " GROUP BY LoaiCamXuc"

    # listEmotion = sql.select(query)
    # print(listEmotion)
    # data = {}
    # for emotion in listEmotion:
    #     data[emotion[0]] = emotion[1]

    # query = "SELECT image FROM dbo.Emotion where"
    # query += "  ThietBi= {} and CONVERT(DATE,Ngay)='{}' and Kip={}".format(
    #     3, datetime.now(), 1)

    # listImage = sql.select(query)
    # data['image'] = [img[0] for img in listImage]

    # print(data)
