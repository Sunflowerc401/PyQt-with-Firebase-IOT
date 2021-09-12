import sys
from PyQt5.QtCore import QRunnable, QThreadPool,QTimer
from PyQt5.uic.uiparser import QtCore
import pyrebase
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
import time


firebaseConfig = { 'apiKey': "AIzaSyA3c8BZTsc0ZtJw5J8r2IoRjBk5-_ktXG8",
  'authDomain': "pyqt-test.firebaseapp.com",
  'databaseURL': "https://pyqt-test-default-rtdb.firebaseio.com",
  'projectId': "pyqt-test",
  'storageBucket': "pyqt-test.appspot.com",
  'messagingSenderId': "107324352003",
  'appId': "1:107324352003:web:746d96dea52b17acd1d036",
  'measurementId': "G-CLPRXNG5YV"}

firebase = pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

door = db.child("Control").child("Door").get().val() # reading data from firebase
run = True
# this thread running in backgroud
class Runnable(QRunnable):
    def __init__(self):
        super().__init__()
    def run(self):
        while run:
            global door
            door = db.child("Control").child("Door").get().val()
            print(door) #this use to check the data recive from firebase (Debug)
            time.sleep(1)
        

class Control_screen(QMainWindow):
    def __init__(self):
        super(Control_screen, self).__init__()
        loadUi("control_screen.ui",self) #Load ui file if the ui in same folder with main code
        self.open_btn.clicked.connect(self.open_data) #if the open button clicked jumb to open_data function
        self.close_btn.clicked.connect(self.close_data)
        app.aboutToQuit.connect(self.close_event) #check if user close the app then jumb to close_even func
    def open_data(self):
        db.child("Control").update({'Door':1})  #send update data to firebase
    def close_data(self):
        db.child("Control").update({'Door':0})
    def update_label(self): #this func try to update the status label if it change
        if (door == 1):
            self.op_label.setText("OPEN")
        elif(door == 0):
            self.op_label.setText("CLOSE")
    def close_event(self): # func use to stop the reading thread
        global run
        run = False


#main

if __name__ == '__main__':
    #thread run
    pool = QThreadPool.globalInstance()
    runnable = Runnable()
    pool.start(runnable)
    #app running
    app = QApplication(sys.argv)
    control = Control_screen()
    widget = QStackedWidget()
    widget.addWidget(control)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    # update label every 1 mili second
    #timer
    timer = QTimer()
    timer.timeout.connect(control.update_label)
    timer.start(1)
    sys.exit(app.exec())
