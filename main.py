from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import sqlite3
import datetime
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import face_recognition
import os
import pandas as pd
import face_recognition
import cv2
import numpy as np
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, NumericProperty
import csv    
from multiprocessing import Process
from wrapt_timeout_decorator import *
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.image import Image, AsyncImage

conn=sqlite3.connect('data.sqlite')
cur=conn.cursor()
cur.execute("DROP TABLE IF EXISTS adata")




class P(Screen):
    pass
    
    
def show_popup():
    show = P()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400),auto_dismiss=True)
    
    popupWindow.open()

    

class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    def redirect(self):
        os.system("registration.py")
        
    

class Studentinfo():
    pass

    
 
class Automatic(Screen):
    known_face_encodings=list()
    known_face_names=list()
    conn=sqlite3.connect('data.sqlite')

    cur=conn.cursor()
    cur.execute("SELECT*FROM sdata")
    a=cur.fetchall()
    lst=list()
    
    
    
    
    for t in a:
        n="student/"+t[3]
        image= face_recognition.load_image_file(n)
        face_encoding=face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(t[1])

    
    
    
    
    def autoterminate(self):
        self.submit()
        
        conn=sqlite3.connect('data.sqlite')
        cur=conn.cursor()
        for name in self.lst:
        
        
            cur.execute('SELECT ROLL_NO FROM sdata where Name=?',(name,))
            b=cur.fetchall()
            
            try:
                cur.execute("CREATE TABLE adata(rno INTEGER,name TEXT)")
                cur.execute('INSERT OR IGNORE INTO adata(rno,name) VALUES(?,?)' ,((b[0][0],name)))
            except:
                cur.execute('INSERT OR IGNORE INTO adata(rno,name) VALUES(?,?)' ,((b[0][0],name)))
        
            
        
        conn.commit()
        t=time.localtime()
                    
        lt=str(time.strftime("%d_%b_%y",t))
        csv_name='records/'+lt+'.csv'
        
        cur.execute("SELECT*FROM adata ORDER BY rno ASC")
       
        a=cur.fetchall()
        with open(csv_name, "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            
            csv_writer.writerows(a)
        
        
        
        unrepeat()
       
      
        self.sucessfullattend()
        
        
    def sucessfullattend(self):
        prompt=""
        for t in self.lst: 
            prompt=prompt+"\n"+t
    
        pop = Popup(title='Registered',
                  content=Label(text=prompt),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
        content = Button(text='OK')
        self.lst.clear()
        sm.current="second"     
        content.bind(on_press=pop.dismiss)              
        pop.open()    
    
    def submit(self):
    
        global name
        
        name="NULL"
        
        video_capture = cv2.VideoCapture(0)
        
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True   
        
        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"  
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]: 
                        name = self.known_face_names[best_match_index]
                    face_names.append(name)                        
        
            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
            
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break     
                       
            if name!='NULL':
                if name not in self.lst:
                    self.lst.append(name)                
        video_capture.release()
        cv2.destroyAllWindows() 




class RegisterWindow(Screen): 

    
    namee = ObjectProperty(None)
    rno= ObjectProperty(None)
    
    
    def submit(self):
        conn=sqlite3.connect('data.sqlite')
        cur=conn.cursor()
        if self.namee.text != "" and self.rno.text !="" :
            try:
                cur.execute('CREATE TABLE IF NOT EXISTS sdata(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Name TEXT,ROLL_NO INTEGER UNIQUE,Photoname TEXT)')
                cur.execute('INSERT OR IGNORE INTO sdata(Name,ROLL_NO,Photoname) VALUES(?,?,?)' ,(self.namee.text,int(self.rno.text),photoname))
            except:
                cur.execute('INSERT OR IGNORE INTO sdata(Name,ROLL_NO,Photoname) VALUES(?,?,?)' ,(self.namee.text,int(self.rno.text),photoname))
            conn.commit()
            sucessfull()
            self.reset()
            sm.current="register"
                
        else:
            invalidForm() 
    def reset(self):
        self.namee.text = ""
        self.rno.text = ""
        photoname = ""            
       
 
class CameraClick(Screen):
    def capture(self):
       
        camera = self.ids['camera']
        global photoname
        timestr = time.strftime("%H%M%S")
        photoname = "IMG_{}.png".format(timestr)
        
        camera.export_to_png(os.path.join("student", photoname))
        show_popup() 

class MannualAttend(Screen):
    namee = ObjectProperty(None)
    rno= ObjectProperty(None)

    def submit(self):
        conn=sqlite3.connect('data.sqlite')
        cur=conn.cursor()
        k=0
        if self.namee.text!="":
            k=k+1
        if k!=0:
            try:
                cur.execute("CREATE TABLE IF NOT EXISTS adata(rno INTEGER,name TEXT)")
                cur.execute('INSERT OR IGNORE INTO adata(rno,name) VALUES(?,?)' ,(int(self.rno.text),self.namee.text))
            except:
                cur.execute('INSERT OR IGNORE INTO adata(rno,name) VALUES(?,?)' ,(int(self.rno.text),self.namee.text))
            
        conn.commit()
        if k==0:
            self.invalidno()
        
        t=time.localtime()
                    
        lt=str(time.strftime("%d_%b_%y",t))
        csv_name='records/'+lt+'.csv'
        
        
        
        if k!=0:
            cur.execute("SELECT*FROM adata ORDER BY rno ASC")
       
        a=cur.fetchall()
        with open(csv_name, "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            
            csv_writer.writerows(a)
        
        self.reset()
        
        sm.current="second"
        if k!=0:
            unrepeat()
            self.sucessfullattend()
        
    def sucessfullattend(self):
    
        pop = Popup(title='Registered',
                  content=Label(text="Attendance Marked"),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
        content = Button(text='OK')              
        content.bind(on_press=pop.dismiss)              
        pop.open()     
    def invalidno(self):
    
        pop = Popup(title='Invalid',
                  content=Label(text="Enter Correct Details"),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
        content = Button(text='OK')              
        content.bind(on_press=pop.dismiss)              
        pop.open()        

    def reset(self):
        self.namee.text=""
        self.rno.text=""



class Studentinfo(Screen):
    rnumber= ObjectProperty(None)
    global sidd
    
    def submit(self):
        k=0
        d=0
        global sidd
        sidd=self.rnumber.text
        conn=sqlite3.connect('data.sqlite')
        cur=conn.cursor()
        cur.execute("SELECT ROLL_NO FROM sdata")
        a=cur.fetchall()
        if self.rnumber.text!="":
            d=d+1
        if d!=0:    
            for i in a:
                if i[0]==int(self.rnumber.text):
                    k=k+1
                    
                    sm.current="view"
        if k==0 or self.rnumber.text=="":        
            self.invalidno()    
    def invalidno(self):
    
        pop = Popup(title='Unregistered',
                  content=Label(text="No Data Found"),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
        content = Button(text='OK')              
        content.bind(on_press=pop.dismiss)              
        pop.open()        
       

class Imageview(Screen):
    namee=ObjectProperty(None)
    rno=ObjectProperty(None)
    def on_enter(self, *args):
        conn=sqlite3.connect('data.sqlite')
        cur=conn.cursor()
        cur.execute('SELECT Name FROM sdata where ROLL_NO=?',(sidd,))
        b=cur.fetchall()
        self.namee.text = "Name :" + b[0][0]
        cur.execute('SELECT Photoname FROM sdata where ROLL_NO=?',(sidd,))
        b=cur.fetchall()
        self.rno.text="Roll Number :" + sidd
        self.ids.imageView.source = 'student/'+b[0][0]
    







class WindowManager(ScreenManager):
    pass
    
    
    
    
    
    
 
def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open() 
 
def sucessfull():
    
    pop = Popup(title='Registered',
                  content=Label(text='successfully registered!'),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
    content = Button(text='OK')              
    content.bind(on_press=pop.dismiss)              
    pop.open()
    
def atmarked():
    
    pop = Popup(title='Registered',
                  content=Label(text="name"),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
    content = Button(text='OK')              
    content.bind(on_press=pop.dismiss)              
    pop.open()    
    
 


def unrepeat():
    
    t=time.localtime()
    lt=str(time.strftime("%d_%b_%y",t))
    conn=sqlite3.connect('data.sqlite')
    cur=conn.cursor()
    cur.execute("DROP TABLE IF EXISTS repeatdata")
    cur.execute("CREATE TABLE IF NOT EXISTS repeatdata(rno INTEGER,name TEXT)")
    csv_name='records/'+lt+'.csv'
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                
                cur.execute('INSERT OR IGNORE INTO repeatdata(rno,name) VALUES(?,?)' ,(int(row[0]),row[1]))
                
            except:
                continue   
    conn.commit()
            
    cur.execute("SELECT DISTINCT rno,name FROM repeatdata ORDER BY rno")       
    a=cur.fetchall()
    os.remove(csv_name)
    with open(csv_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
            
        csv_writer.writerows(a)

 
 
 

    

kv = Builder.load_file("my.kv")
sm = WindowManager()
try:
    screens=[SecondWindow(name="second"),Studentinfo(name="detail"),Imageview(name="view"),RegisterWindow(name="register"),Automatic(name="autoattend"),MannualAttend(name="manattend"),MainWindow(name="main")]
    for screen in screens:
        sm.add_widget(screen)
except: 
    screens=[SecondWindow(name="second"),Studentinfo(name="detail"),Imageview(name="view"),RegisterWindow(name="register"),CameraClick(name="click"),Automatic(name="autoattend"),MannualAttend(name="manattend"),MainWindow(name="main")] 
    for screen in screens:
        sm.add_widget(screen)    
sm.current="main"

class MyMainApp(App):
    title = 'Attendance'
    icon = 'icon.png'
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()