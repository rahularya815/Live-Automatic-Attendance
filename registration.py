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
        
        
class P(Screen):
    pass
    
    
def show_popup():
    show = P()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400),auto_dismiss=True)
    show.bind(on_press=popupWindow.dismiss)
    popupWindow.open()
 

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
    content.bind(on_press= lambda: self.popup_exit.dismiss())              
    pop.open()
    
def atmarked():
    
    pop = Popup(title='Registered',
                  content=Label(text="name"),
                  size_hint=(None, None), size=(400, 400),auto_dismiss=True)
    content = Button(text='OK')              
    content.bind(on_press=pop.dismiss)              
    pop.open()    
    
 



 
kv = Builder.load_file("register.kv")
sm = WindowManager()   


screens=[RegisterWindow(name="register"),CameraClick(name="click")] 
for screen in screens:
    sm.add_widget(screen)    
sm.current="register"

class MyMainApp(App):
    title = 'Registration'
    icon = 'icon.png'
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()     