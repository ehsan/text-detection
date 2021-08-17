import os,sys
import numpy as np
import cv2

# author: qzane@live.com
# reference: http://stackoverflow.com/a/23565051
# further reading: http://docs.opencv.org/master/da/d56/group__text__detect.html#gsc.tab=0
def text_detect(img,ele_size=(8,2)): #
    if len(img.shape)==3:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_sobel = cv2.Sobel(img,cv2.CV_8U,1,0)#same as default,None,3,1,0,cv2.BORDER_DEFAULT)
    img_threshold = cv2.threshold(img_sobel,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
    img_threshold = cv2.morphologyEx(img_threshold[1],cv2.MORPH_CLOSE,element)
    res = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if cv2.__version__.split(".")[0] == '3':
        _, contours, hierarchy = res
    else:
        contours, hierarchy = res
    Rect = [cv2.boundingRect(i) for i in contours if i.shape[0]>100]
    RectP = [(int(i[0]-i[2]*0.08),int(i[1]-i[3]*0.08),int(i[0]+i[2]*1.1),int(i[1]+i[3]*1.1)) for i in Rect]
    return RectP

def get_leftColumn(rect):
    leftColumn = [i for i in filter(lambda i : i[2] < 180, rect)]
    leftColumn.sort(key=lambda i : (i[1], i[0]), reverse=False)
    return leftColumn

def get_rightColumn(rect):
    rightColumn = [i for i in filter(lambda i : i[0] > 1880, rect)]
    rightColumn.sort(key=lambda i : (i[1], i[0]), reverse=False)
    return rightColumn

def get_midRow(rect):
    midRow = [i for i in filter(lambda i : i[1] > 1000 and i[1] < 1250 and i[0] > 600 and i[2] < 1400, rect)]
    midRow.sort(key=lambda i : (i[1], i[0]), reverse=False)
    return midRow

def x_main(rect, _, __):
    leftColumn = [i for i in get_leftColumn(rect)]
    if (len(leftColumn) > 5):
        print(leftColumn[5])

def new_address(rect, _, __):
    rightColumn = [i for i in get_rightColumn(rect)]
    if (len(rightColumn) > 15):
        print(rightColumn[13])
        print(rightColumn[15])

def startup(rect, _, __):
    midRow = [i for i in get_midRow(rect)]
    if (len(midRow) > 4):
        print(midRow[4])

def squint(rect, _, __):
    leftColumn = get_leftColumn(rect)
    midRow = get_midRow(rect)
    if (len(leftColumn) == 0):
        print("startup")
    elif (len(midRow) == 0):
        print("main")
    else:
        print("wallet")

def default(rect, img, outputFile):
    for i in rect:
        cv2.rectangle(img,i[:2],i[2:],(0,0,255))
    cv2.imwrite(outputFile, img)

def main(inputFile, which):
    outputFile = inputFile.split('.')[0]+'-rect.'+'.'.join(inputFile.split('.')[1:])
    img = cv2.imread(inputFile)
    rect = text_detect(img,(12,4))
    switcher = {
      "--main": "x_main",
      "--new-address": "new_address",
      "--startup": "startup",
      "--squint": "squint",
    }
    func = switcher.get(which, "default")
    eval("%s(rect, img, outputFile)" % func)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else '')
