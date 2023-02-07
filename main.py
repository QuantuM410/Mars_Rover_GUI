from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtCore import QTime

from Mars_Image_Extractor import Mars_Image_Extrator_Widget

import sys

bgimg = """
    MainWindow {
        background-image: url("/home/quantum410/Mars_rover_app/sources/night-sky-background-with-stars_104785-147.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }   
"""

app = QApplication(sys.argv)
app.setStyleSheet(bgimg)
window = Mars_Image_Extrator_Widget()
window.show() 

app.exec()