from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QComboBox, QHBoxLayout
from PySide6.QtGui import QPixmap
import PySide6.QtCore, PySide6.QtWidgets
from PySide6.QtCore import QRect
import os , glob

import requests
import urllib.request
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow
from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor



api_key = "tFjDsN6xmhOv3qddajpirPCa8kdoRVwjtUPOYILw"

class Mars_Image_Extrator_Widget(QMainWindow,QWidget) :
    def __init__(self):
        super().__init__()
        
     
        self.setFixedSize(800,600)
        self.setWindowTitle("Mars Rover Image Extractor")


        self.dateedit = PySide6.QtWidgets.QDateEdit(calendarPopup=True)
        
        self.menuBar().setCornerWidget(self.dateedit, PySide6.QtCore.Qt.Corner.TopLeftCorner)
        self.dateedit.setDateTime(PySide6.QtCore.QDateTime.currentDateTime())
        
        global dateedit
        

        self.camera_label = QLabel(self)
        self.camera_label.setText("Camera :")
        self.camera_label.setGeometry(50,30,60,30)
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("FHAZ")
        self.combo_box.addItem("RHAZ")
        self.combo_box.addItem("MAST")
        self.combo_box.addItem("CHEMCAM")
        self.combo_box.addItem("MAHLI")
        self.combo_box.addItem("MARDI")
        self.combo_box.addItem("NAVCAM")
        self.combo_box.setGeometry(110,30,100,30)
        
        global combo_box
        
        
        

        self.Fetch_Image_Button = QPushButton('Fetch Images',self)
        self.Fetch_Image_Button.setGeometry(150,400,500,30)

        
        Next_Push_Button = QPushButton('<<',self)
        Next_Push_Button.setGeometry(50,400,100,30)
        Prev_Push_Button = QPushButton('>>',self)   
        Prev_Push_Button.setGeometry(650,400,100,30)


        self.Fetch_Image_Button.clicked.connect(self.APImage_fetcher)
        


    def APImage_fetcher(self) :
        print("working?")
        camera = self.combo_box.currentText()
        earth_date_object = self.dateedit.date()
        earth_date_python_object = earth_date_object.toPython()
        earth_date_param = earth_date_python_object.strftime('%Y-%m-%d')
        
        
        to_be_deleted_files = glob.glob('/images/*') #to be used if used input image count from user
        for f in to_be_deleted_files:
            os.remove(f)
            print('deleted')
        
        parameters = [camera , earth_date_param]
        print(parameters)
        
        api_key = "F9n23eGLM1DR8NPgsUODYHxGlradvr7FpHJYRoxR"
        base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date="+parameters[1]+"&camera="+parameters[0]+"&api_key="+api_key
        response = requests.get(base_url)
        data = response.json()
      
        
        images = []
        try :
            if len(data) <= 10 :
                image_count = len(data['photos'])
            else :
                image_count = 10

            for i in range(image_count) :
                img_source = data['photos'][i]['img_src']
                images.append(img_source)
                urllib.request.urlretrieve(images[i], "images/image{}.jpg".format(i))

            print("finished fetching . . .")
            self.initUI()
        except IndexError :
            print("No Matched Images as per the PARAMETERS assigned")

    def initUI(self):       

        self.image_label = QLabel(self)
        #self.image_label.setGeometry(QRect(110,50,100,100))
        self.pixmap = QPixmap('images/image0.jpg')
        self.image_label.setPixmap(self.pixmap)
        self.setCentralWidget(self.image_label)
        
        print("is it working?")                                                                                                 




            


    



    