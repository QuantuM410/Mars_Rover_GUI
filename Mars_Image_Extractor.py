from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QLineEdit, QSizePolicy, QGridLayout, QTextEdit
from PySide6.QtGui import QPixmap, QMovie, QIcon
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
        self.setStyleSheet("background-color:#175776")
        global multiparentlayout
        global buttonimagelayout
        mainlayout = QVBoxLayout()
        buttonimagelayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        prevnextlayout = QHBoxLayout()
        sideandmainlayout = QHBoxLayout()
        

        self.setFixedSize(800,600)
        self.setWindowTitle("Mars Rover Image Extractor")


        self.dateedit = PySide6.QtWidgets.QDateEdit(calendarPopup=True)
        
        #self.menuBar().setCornerWidget(self.dateedit, PySide6.QtCore.Qt.Corner.TopLeftCorner)
        self.dateedit.setDateTime(PySide6.QtCore.QDateTime.currentDateTime())
        self.dateedit.setStyleSheet('background-color:#01101f')

        global dateedit
        
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("FHAZ")
        self.combo_box.addItem("RHAZ")
        self.combo_box.addItem("MAST")
        self.combo_box.addItem("CHEMCAM")
        self.combo_box.addItem("MAHLI")
        self.combo_box.addItem("MARDI")
        self.combo_box.addItem("NAVCAM")
        self.combo_box.setStyleSheet('background-color: #01101f')
        #self.combo_box.setGeometry(150,130,100,30)
        
        global combo_box
        
        
        
        self.Fetch_Image_Button = QPushButton('Fetch Images',self)
        self.Fetch_Image_Button.setStyleSheet('''background-color: #01101f''')
        #self.Fetch_Image_Button.setGeometry(150,250,100,40)

        
        self.Next_Push_Button = QPushButton('>>',self)
        self.Next_Push_Button.setGeometry(150,400,100,40)
        self.Next_Push_Button.setStyleSheet("background-color: #01101f")
        self.Prev_Push_Button = QPushButton('<<',self)   
        self.Prev_Push_Button.setGeometry(50,400,100,40)
        self.Prev_Push_Button.setStyleSheet("background-color: #01101f")

        self.Mail_Button = QPushButton('Mail', self)
        self.Mail_Button.setStyleSheet('background-color: #01101f')
        #self.Mail_Button.setGeometry(250,400,100,40)


        self.Fetch_Image_Button.clicked.connect(self.APImage_fetcher)
        self.Next_Push_Button.clicked.connect(self.next)
        self.Prev_Push_Button.clicked.connect(self.prev)
        self.Mail_Button.clicked.connect(self.mail)

        buttonlayout.addWidget(self.dateedit)
        buttonlayout.addWidget(self.combo_box)
        buttonlayout.addWidget(self.Fetch_Image_Button)
        buttonlayout.addWidget(self.Mail_Button)

        prevnextlayout.addWidget(self.Prev_Push_Button)
        prevnextlayout.addWidget(self.Next_Push_Button)

        global mainimagelabel
        mainimagelabel = QLabel(self)
        self.movie = QMovie("sources/image_processing20200606-21890-swfktj.gif")
        mainimagelabel.setMovie(self.movie)
        mainimagelabel.setScaledContents(True)
        self.movie.start()

        buttonimagelayout.addLayout(buttonlayout)
        buttonimagelayout.addWidget(mainimagelabel)
        buttonimagelayout.addLayout(prevnextlayout)

        sidebar = QLabel(self)
        self.movie = QMovie("sources/16759164434838555564708490698427.gif")
        sidebar.setMovie(self.movie)
        sidebar.setScaledContents(True)
        self.movie.start()
    
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color:#B9D1D0")

        sideandmainlayout.addLayout(buttonimagelayout)
        sideandmainlayout.addWidget(sidebar)

        topbarlabel = QLabel(self)
        self.movie = QMovie("sources/mars_header_3_0.gif")
        topbarlabel.setMovie(self.movie)
        topbarlabel.setScaledContents(True)
        topbarlabel.setFixedHeight(100)
        self.movie.start()

        mainlayout.addWidget(topbarlabel)
        mainlayout.addLayout(sideandmainlayout)

        #parent_layout.addLayout(image_layout)
        global centralWidget
        centralWidget = QWidget()
        centralWidget.setLayout(mainlayout)

        self.setCentralWidget(centralWidget)

        


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

            if image_count != 0 :
                for i in range(image_count) :
                    img_source = data['photos'][i]['img_src']
                    images.append(img_source)
                    urllib.request.urlretrieve(images[i], "images/image{}.jpg".format(i))

                print("finished fetching . . .")
            

                self.initUI()
            else :

                self.pixmap = QPixmap("sources/HTML-404-Error-Page.png")
                mainimagelabel.setPixmap(self.pixmap)
                mainimagelabel.setScaledContents(True)
                



            
        except Exception as e :
            print(e)

    def initUI(self):       

        #self.image_label.setGeometry(QRect(110,50,100,100))
        global count
        count = 0
        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        #self.pixmap = self.pixmap.scaled(800,600)
        mainimagelabel.setPixmap(self.pixmap)
        self.setCentralWidget(centralWidget)
        
        




        
        #parent_layout.addWidget(self.image_label)

        #self.setCentralWidget(self.image_label)
    # self.section_layout.addWidget(self.image_label)
        
        
        
        #self.image_label.setGeometry(300,100,400,400)
        
        #self.image_label.setGeometry()
        
                                                                                        


    def next(self) :
        global count
        count += 1
        if count > image_count-1 :
            count = 0
        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        mainimagelabel.setPixmap(self.pixmap)
        self.setCentralWidget(centralWidget)
    
    
    def prev(self) :
        global count
        count -= 1
        if count < 0 :
            count = image_count-1

        self.pixmap = QPixmap('images/image{}.jpg'.format(count))
        mainimagelabel.setPixmap(self.pixmap)
        self.setCentralWidget(centralWidget)

    
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

        self.setStyleSheet("background-color:#175776")
        

        maillayout = QGridLayout()
        maillayout.setSpacing(10)
        #fro = QLabel("From")
        to = QLabel("To")
        Subjec = QLabel("Subject")
        Messa = QLabel("Message")

        #global fromuser
        #self.fromuser = QLineEdit(self)
        global touser
        self.touser = QLineEdit(self)
        self.touser.setStyleSheet("background-color: #01101f")
        global subject
        self.subject = QLineEdit(self)
        self.subject.setStyleSheet("background-color: #01101f")
        global message
        self.message = QTextEdit(self)
        self.message.setStyleSheet("background-color: #01101f")

        self.confirm = QPushButton('confirm',self)
        self.confirm.setStyleSheet("background-color: #01101f")

        self.confirm.clicked.connect(self.sendmail)
        
        #maillayout.addWidget(fro, 2, 0)
        #maillayout.addWidget(self.fromuser, 2, 1)
        maillayout.addWidget(to, 3, 0)
        maillayout.addWidget(self.touser, 3, 1)
        maillayout.addWidget(Subjec, 4, 0)
        maillayout.addWidget(self.subject, 4, 1)
        maillayout.addWidget(Messa, 5, 0)
        maillayout.addWidget(self.message, 5, 1, 5, 1)
        maillayout.addWidget(self.confirm, 11,1)
        maillayout.setContentsMargins(20,20,20,50)
        maillayout.setColumnStretch(1,5)
        mailwidget = QWidget()
        mailwidget.setLayout(maillayout)
        self.setCentralWidget(mailwidget)
        self.setGeometry(400,200,600,500)

    
    def sendmail(self) :
        
        smtp_port = 587
        smtp_server = "smtp.gmail.com"
        fromail = "kartikeys410@gmail.com"
        tomail = self.touser.text()
        tomail = tomail.split(",")
        subjectdata = self.subject.text()
        messagebody = self.message.toPlainText()


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

    def mailsentdialog(self) :
        self.window = Mailsent()
        self.window.show()









            


    



    