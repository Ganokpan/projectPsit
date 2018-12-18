#-*- coding=utf-8 -*-
import ast
import mysql.connector
from flask import Flask
from flask import render_template
from flask import request

#ใข้ framework flask ในการทำ
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/save', methods=['GET'])
def save(): #โมดูลแสดงข้อมูล
    #รับข้อมูลจาก home.html โดนส่งเป็น method GET ผ่าน URL
        #กำหนดตัวแปร rawdata คือ dict ที่รับมาจาก request URL website
    name, contact, imgurl, answer, rawdata = '', '', '', '', dict(request.args)
        # (name contact imgurl)คือตัวแปรจะถูกเพิ่มค่าจาก dict rawdata
        #โดยผ่านเงื่อนไข ด้านล่าง
    for i in rawdata:
        if i == 'name':
            name = rawdata[i].pop()
        elif i == 'contact':
            contact = rawdata[i].pop()
        elif i == 'imgurl':
            imgurl = rawdata[i].pop()
        else:
            answer += rawdata[i].pop() #นำคำตอบมาเรียงกันเช่น
    #เมื่อได้เพิ่มค่าให้ตัวแปรเรียบร้อยก็จะเป็นส่วนของการ conect เข้า server
    #เป็นค่าของตัวแปรข้องบนที่กำหนดไว้ ส่งเข้าฐานข้อมูลตามตาราง
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="mydatabase"
    )
    mycursor = mydb.cursor()
    # นำค่าจากตัวแปรใส่ลงไปใน Field ที่ต้องการจัดเก็บ
    sql = "INSERT INTO customers (name, contact, imgurl, answer_1) VALUES (%s, %s, %s, %s)"
    val = (name, contact, imgurl, answer)
    mycursor.execute(sql, val)
    mydb.commit()
    #ส่วนนี้จะเป็นการกำหนด % ของจำนวนคนที่ตอบเหมือนเรา โดย คิดจาก
    mycursor.execute("SELECT answer_1 FROM customers")
    myresult = mycursor.fetchall()
    allans = 0 #จำนวนผู้ตอบคำถามทั้งหมด
    match = 0 #จำนวนผู้ตอบคำถามเหมือนคุณทั้งหมด
    for x in myresult:
        if x != ('',):#จำนวนคนที่ตอบทั้งหมด
            allans += 1
            if x[0] == answer:#จำนวนคนที่ตอบเหมือนเรา
                match += 1
    match = match*(100/allans)#คิดเป็น %
    #ทำการส่งออกค่าที่จะใช้แสดงผลในหน้าต่อไป
    return getData(mydb, mycursor, name, contact, imgurl, answer, match)

@app.route('/save', methods=['GET'])
def getData(mydb, mycursor, name, contact, imgurl, answer, match):
    likeu = [] #กำหนดตัวแปรเก็บ list ผู้คนที่ตอบเหมือนเรา
    #หาจาก database โดย Field ที่ answer_1 เท่ากับ คำตอบของเรา(answer)
    sql = ("SELECT * FROM customers WHERE answer_1 = %s" %answer)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    #นำค่าคนที่ตอบเหมือนเรา มาเก็บใน dict อีกทีแบ่งเป็นแต่ละคน
    #เพื่อนำมากระจายลงไป ในไฟล์ home.html ที่ได้ทำ form ไว้เพื่อให้เกิดระเบียบ
    for x in myresult:
        likeu.append({'name': x[0] , 'contact': x[1], 'imgurl': x[2]})
    return render_template('chart.html', likeu=likeu, name=name, imgurl=imgurl, match="%.1f"%match)

app.run(debug=True,port=80)
