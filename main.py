from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets , QtCore , QtGui, uic
import sys
import numpy as np
import cv2
from PIL import Image
import sys
from JpegReader import JPEGFileReader
from Decoder import Ui_MainWindow 


class ApplicationWindow(QtWidgets.QMainWindow):
    MyBrowse=['']

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.pushButton_handler)
        self.labels=[self.ui.label_2,self.ui.label_3, self.ui.label_4, self.ui.label_5, self.ui.label_6, self.ui.label_7, self.ui.label_8, self.ui.label_9]
        self.ui.Decode_button.setEnabled(0)

        self.ui.Decode_button.clicked.connect(self.Decoding)


        self.Output=['Output/output1.jpeg','Output/output2.jpeg','Output/output3.jpeg','Output/output4.jpeg','Output/output5.jpeg','Output/output6.jpeg','Output/output7.jpeg','Output/output8.jpeg']


    def pushButton_handler(self):
        self.open_dialoge_box()
    def open_dialoge_box(self):

        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.MyBrowse = path
        self.Open_Img()
        print(self.MyBrowse)


    def Open_Img(self):

        self.image=QtGui.QImage(self.MyBrowse)
        self.pixmapImage=QtGui.QPixmap.fromImage(self.image).scaled(250,250)
        #show the image
        self.ui.label.setPixmap(self.pixmapImage)
        self.ui.Decode_button.setEnabled(1)

            
    def Decoding (self):
        
        Marker= JPEGFileReader(self.MyBrowse)
        Marker.ReadingJpeg()
        Marker.QuantizationTable()
        Marker.HuffmanTable()
        Indices= Marker.GetMarkerIndex('ffda')
        for i in range (8):
            JpegByte=open(self.MyBrowse,"rb").read(Indices[i+1])
            jpegData2 = open(self.Output[i],"wb")
            jpegData2.write(JpegByte)
            jpegData2.write(b'\xff\xd9')
            jpegData2.close()
            self.image=QtGui.QImage(self.Output[i])
            self.pixmapImage=QtGui.QPixmap.fromImage(self.image).scaled(250,250)            
            self.labels[i].setPixmap(self.pixmapImage)




        
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
