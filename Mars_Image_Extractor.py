from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide6.QtGui import QPixmap
import PySide6.QtCore, PySide6.QtWidgets
from PySide6.QtCore import QRect, Qt, QSize, QRunnable
import os , glob
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import urllib.request
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow
from PySide6.QtGui import QPixmap

from PySide6.QtGui import QCursor



api_key = "tFjDsN6xmhOv3qddajpirPCa8kdoRVwjtUPOYILw"

class Mars_Image_Extrator_Widget(QMainWindow,QWidget,QRunnable) :
    def __init__(self):
        super().__init__()
        
     
        self.setFixedSize(1280,720)
        self.setWindowTitle("Mars Rover Image Extractor")


        self.dateedit = PySide6.QtWidgets.QDateEdit(calendarPopup=True)
        
        self.menuBar().setCornerWidget(self.dateedit, PySide6.QtCore.Qt.Corner.TopLeftCorner)
        self.dateedit.setDateTime(PySide6.QtCore.QDateTime.currentDateTime())
        

        global dateedit
        

        self.camera_label = QLabel(self)
        self.camera_label.setText("Camera :")
        self.camera_label.setGeometry(50,130,60,30)
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("FHAZ")
        self.combo_box.addItem("RHAZ")
        self.combo_box.addItem("MAST")
        self.combo_box.addItem("CHEMCAM")
        self.combo_box.addItem("MAHLI")
        self.combo_box.addItem("MARDI")
        self.combo_box.addItem("NAVCAM")
        self.combo_box.setGeometry(150,130,100,30)
        
        global combo_box
        
        
        
        self.fetch_button_label = QLabel(self)
        self.fetch_button_label.setText("Fetch Images :")
        self.fetch_button_label.setGeometry(50,250,100,40)
        self.Fetch_Image_Button = QPushButton('Fetch Images',self)
        self.Fetch_Image_Button.setGeometry(150,250,100,40)

        
        self.Next_Push_Button = QPushButton('>>',self)
        self.Next_Push_Button.setGeometry(150,400,100,40)
        self.Prev_Push_Button = QPushButton('<<',self)   
        self.Prev_Push_Button.setGeometry(50,400,100,40)

        self.Mail_Button = QPushButton('Mail', self)
        self.Mail_Button.setGeometry(250,400,100,40)


        self.Fetch_Image_Button.clicked.connect(self.APImage_fetcher)
        self.Next_Push_Button.clicked.connect(self.next)
        self.Prev_Push_Button.clicked.connect(self.prev)
        self.Mail_Button.clicked.connect(self.mail)


    def APImage_fetcher(self) :
        camera = self.combo_box.currentText()
        earth_date_object = self.dateedit.date()
        earth_date_python_object = earth_date_object.toPython()
        earth_date_param = earth_date_python_object.strftime('%Y-%m-%d')
        
        
        to_be_deleted_files = glob.glob('/home/quantum410/Mars_rover_app/images/*') #to be used if used input image count from user
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
        global image_count
        try :
            if len(data['photos']) <= 10 :
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
        global count
        count = 0
        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        self.pixmap = self.pixmap.scaled(800,600)
        self.image_label.setPixmap(self.pixmap)
        self.setCentralWidget(self.image_label)
        self.image_label.setFixedSize(100,100)
        
        
        
        
        #self.image_label.setGeometry(300,100,400,400)
        
        #self.image_label.setGeometry()
        
                                                                                          


    def next(self) :
        global count
        count += 1
        if count > image_count-1 :
            count = 0
        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        self.image_label.setPixmap(self.pixmap)
        self.setCentralWidget(self.image_label)
        self.image_label.setFixedSize(100,100)
    
    def prev(self) :
        global count
        count -= 1
        if count < 0 :
            count = image_count-1

        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        self.image_label.setPixmap(self.pixmap)
        self.setCentralWidget(self.image_label)
        self.image_label.setFixedSize(100,100)
    
    def mail(self) :
        maillayout = QVBoxLayout()
        self.fromuser = QLineEdit()
        self.touser = QLineEdit()
        self.subject = QLineEdit()
        maillayout.addWidget(self.fromuser)
        maillayout.addWidget(self.touser)
        maillayout.addWidget(self.subject)
        self.window = Mail()
        self.window.show()

class Mail(QMainWindow,QWidget) :
    def __init__(self):
        super().__init__()

        maillayout = QVBoxLayout()
        mailwidget = QWidget()
        global fromuser
        self.fromuser = QLineEdit(self)
        global touser
        self.touser = QLineEdit(self)
        global subject
        self.subject = QLineEdit(self)
        global message
        self.message = QLineEdit(self)

        self.confirm = QPushButton('confirm',self)

        self.confirm.clicked.connect(self.sendmail)
        
        maillayout.addWidget(self.fromuser)
        maillayout.addWidget(self.touser)
        maillayout.addWidget(self.subject)
        maillayout.addWidget(self.message)
        maillayout.addWidget(self.confirm)
        mailwidget.setLayout(maillayout)
        self.setCentralWidget(mailwidget)
        self.setGeometry(400,200,600,600)

    
    def sendmail(self) :
        
        smtp_port = 587
        smtp_server = "smtp.gmail.com"
        fromail = self.fromuser.text()
        tomail = self.touser.text()
        tomail = tomail.split(",")
        subjectdata = self.subject.text()
        messagebody = self.message.text()


        pswd = "szeewngpejiwydjy"


        for person in tomail :
            msg = MIMEMultipart()
            msg['From'] = fromail.strip()
            msg['To'] = person.strip()
            msg['Subject'] = subjectdata
            msg.attach(MIMEText(messagebody, 'plain'))

            attachmentsloc = glob.glob('/home/quantum410/Mars_rover_app/images/*')

            for image in attachmentsloc :
                attachment = open(image, 'rb')
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload((attachment).read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition', 'attachment; filename= '+image)
                msg.attach(attachment_package)

                msgstr = msg.as_string()

            print('connecting to server ...')    
            TIE_server = smtplib.SMTP(smtp_server,smtp_port)
            TIE_server.starttls()
            TIE_server.login(fromail, pswd)
            print("succesfully connected to server")
            print("sending mail")
            TIE_server.sendmail(fromail.strip(), person.strip(), msgstr)
            print("email sent")
        
        TIE_server.quit()











            


    



    