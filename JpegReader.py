# import argparse
import math
import numpy as np
# from utils import *
# from scipy import fftpack
from PIL import Image
import struct


class JPEGFileReader:



    def __init__(self, filepath):

        #Huffman table needed data

        self.MarkerIndex=[]
        self.upNibble=[]
        self.ID=[]
        self.HuffmanDCTable=[0]*4
        self.HuffmanACTable=[0]*8

        self.AcTables=["========First Ac Table========","========Second Ac Table========","========Third Ac Table========","========Fourth Ac Table========","========Fifth Ac Table========","========Sixth Ac Table========","========Seventh Ac Table========","========eighth Ac Table========"]
        self.DcTables=["========First Dc Table========","========Second Dc Table========"]

        #indices of the the zigzag

        self.zigZagMap=[0 , 1 , 8 ,16 , 9 , 2 , 3 ,10, 17 ,24 ,32 ,25 ,18 ,11 , 4 , 5, 12 ,19 ,26 ,33 ,40 ,48 ,41 ,34, 27 ,20 ,13 , 6 , 7 ,14 ,21 ,28, 35, 42 ,49 ,56 ,57 ,50 ,43 ,36, 29 ,22 ,15 ,23 ,30 ,37 ,44 ,51, 58 ,59 ,52 ,45 ,38 ,31 ,39 , 46, 53 ,60 ,61 ,54 ,47 ,55 ,62 ,63]
        
        self.path = filepath
        

        #function to read the Jpeg header file byte by byte

    def ReadingJpeg(self):

        self.jpegData = open(self.path, 'rb').read()
        self.jpegData = ''.join(['%02x,%02x,' % (self.jpegData[2*i], self.jpegData[2*i+1]) for i in range(len(self.jpegData)>>1)])
        self.jpegData = self.jpegData.split(',')[:-1]


        #function that get the quantization table

    def QuantizationTable (self):    
        self.img=Image.open(self.path)
        self.Qtable= self.img.quantization

        self.QT1=[1]*64
        self.QT2=[1]*64
        for i in range (64):
            self.QT1[self.zigZagMap[i]]=self.Qtable[0][i]
            self.QT2[self.zigZagMap[i]]=self.Qtable[1][i]
        
        print('\n')
        print("||||||||||||First Quantization Table||||||||||||")
        print(self.QT1)
        print('\n')
        print("||||||||||||Second Quantization Table||||||||||||")
        print(self.QT2)
        print('\n')

        return self.QT1 , self.QT2

        #function that get the indices of any marker in the header file

    def GetMarkerIndex(self,marker:str):
        self.index=[]
        for i in range (len(self.jpegData)-1):
            if (marker==self.jpegData[i]+self.jpegData[i+1]):
                self.index.append(i)

        return self.index

        #function that get the huffman (DC-AC) tables

    def HuffmanTable(self):
        length=[]   
        valuesLegnth=[]
        byteSymbols=[]
        AcID=[]
        for m in range (8):
            AcID.append(m)
        
        self.MarkerIndex=self.GetMarkerIndex("ffc4")
        # print(self.MarkerIndex)
        for i in range (len(self.MarkerIndex)):

            byteOffset=[]
            
            x=list(self.jpegData[self.MarkerIndex[i]+4])
            # print(x)
            self.upNibble.append(x[0])
            self.ID.append(x[1])

            y=int(self.jpegData[self.MarkerIndex[i]+2]+self.jpegData[self.MarkerIndex[i]+3],16)
            length.append(y)

            for j in range (16):
               offset=int(self.jpegData[self.MarkerIndex[i]+5+j],16) 
               byteOffset.append(offset)
            
            valuesLegnth.append(byteOffset[15])
            currentIndex=self.MarkerIndex[i]+21
            # print(byteOffset)
            subSymbols = []
            for k in range (16):
                
                subSymbols.append(self.jpegData[currentIndex:currentIndex+byteOffset[k]])
                currentIndex+=byteOffset[k]
            byteSymbols.append(subSymbols)
            
            if (self.upNibble[i]=='0'):
                self.HuffmanDCTable[int(self.ID[i])]=byteSymbols[i]
            elif(self.upNibble[i]=='1'):
                self.HuffmanACTable[AcID[i-2]]=byteSymbols[i]
        
        print('\n')
        print('||||||||||||||| HUFFMAN DC TABLES |||||||||||||||')
        print('\n')
        #####################################################
        for x in range (len(self.HuffmanDCTable)-2):
            print(self.DcTables[x])            
            for y in range (16):
                print(self.HuffmanDCTable[x][y])

        #######################################################
        print('\n')
        print('||||||||||||||| HUFFMAN AC TABLES |||||||||||||||')
        print('\n')

        #####################################################
        for x in range (len(self.HuffmanACTable)):
            print(self.AcTables[x])            
            for y in range (16):
                print(self.HuffmanACTable[x][y])

        #######################################################
