from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtCore import QTime
from PySide6.QtGui import QIcon

from Mars_Image_Extractor import Mars_Image_Extrator_Widget

import sys



app = QApplication(sys.argv)
window = Mars_Image_Extrator_Widget()
window.show() 

app.exec()