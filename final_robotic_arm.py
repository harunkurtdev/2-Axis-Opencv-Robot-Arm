import cv2
import numpy as np
#import serial
import time

##Capture the video
cap = cv2.VideoCapture(0)

# Robotik Kol Çalışması İçin Arduino'ya Seri Pyfirmata Transferi
#from pyfirmata import Arduino,util
#board = Arduino('COM9')


# kameranın kolonu için x ekseni uzunluğunu tanımlayın
x_cm = 23.4    #CHANGE IT
#kamera sırası için y ekseni uzunluğunu tanımlayın
y_cm = 17    #CHANGE IT

while True:

    #iterator = util.Iterator(board)
    #iterator.start()
    _,frame2 = cap.read()
    _, frame1 = cap.read()

    grey_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    grey_image_2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame2)

    cv2.imshow('frame2',grey_image_2)
    cv2.imshow('frame1', grey_image_1)

    diff = np.absolute(np.matrix(np.int16(grey_image_2))-np.matrix(np.int16(grey_image_1)))

    diff[diff>255] = 255
    diff= np.uint8(diff)
    
    """
    mask = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(diff,cv2.MORPH_OPEN,mask)
     _,label = cv2.connectedComponents(diff,connectivity = 4)
    """
    cv2.imshow('difference',diff)
    
    BW = diff
    BW[BW<30] = 0
    BW[BW>=30] = 255
    cv2.imshow('BW', BW)

    # X EKSENİ
    col_add = np.matrix(np.sum(BW, 0))
    # print('col_add',col_add)
    col_no = np.matrix(np.arange(640))  # resimdeki toplam sütun
    # print('col_no',col_no)
    col_mul = np.multiply(col_add, col_no)
    # print('col_mul',col_mul)
    tot_col = np.sum(col_mul)
    # print('tot_col',tot_col)
    tot_col_add = np.sum(col_add)
    # print('tot_col_add',tot_col_add)
    col_px = tot_col / tot_col_add
    # print ('column pixel',col_px)

    # col_px= tot_col/tot_col_add
    # print('col_pixel',col_px)

    # Y EKSENİ
    row_add = np.matrix(np.sum(BW, 1))
    row_add = row_add.transpose()
    row_no = np.matrix(np.arange(480))  # resimdeki toplam sütun
    row_mul = np.multiply(row_add, row_no)
    tot_row = np.sum(row_mul)
    tot_row_add = np.sum(np.sum(BW))
    row_px = tot_row / tot_row_add

    # bunu y eksenini veren cm'ye dönüştür
    y_axis = (y_cm / 480) * row_px
    print('row_pixel', row_px)
    print('y_Axis', y_axis)
    # bunu x eksenini veren cm'ye dönüştür
    x_axis = (x_cm / 640) * col_px
    print('coloumn pixel', col_px)
    print('x_Axis cm', x_axis)

    # ledpin = board.get_pin('d:13:o')
    # dirx = board.get_pin('d:11:o')
    # steppinx = board.get_pin('d:10:o')
    # ms1x = board.get_pin('d:13:o')
    # ms2x = board.get_pin('d:12:o')
    # sleepx = board.get_pin('d:9:o')
    #
    # diry = board.get_pin('d:3:o')
    # steppiny = board.get_pin('d:4:o')
    # ms1y = board.get_pin('d:6:o')
    # ms2y = board.get_pin('d:5:o')
    # sleepy = board.get_pin('d:7:o')
    #
    # # Kolay sürücüyü hem x hem de y uyanık hale getirin
    # sleepx.write(1.0)
    # time.sleep(0.1)
    # sleepy.write(1.0)
    # time.sleep(0.1)
    # x eksenindeki yarım adım için # MS1 = YÜKSEK ve MS2 = DÜŞÜK
    # ms1x.write(1.0)
    # ms2x.write(0.0)
    #
    # y eksenindeki yarım adım için # MS1 = YÜKSEK ve MS2 = DÜŞÜK
    # ms1y.write(1.0)
    # ms2y.write(0.0)
    #
    # Y_AXIS = y_axis * 100 + 90  # çünkü y_axis tabanından bu kadar uzak
    # Y_AXIS = int(Y_AXIS)
    # X_AXIS = x_axis * 100 + 360  # çünkü x_axis tabanından bu kadar uzak
    # X_AXIS = int(X_AXIS)
    # print('Y_AXIS', Y_AXIS)
    # print('X_AXIS', X_AXIS)
    #
    # dirx.write(1.0)  # X steppper saat yönünde (nesneyi seçmek için)
    # diry.write(1.0)  # Y kademeli saat yönünde (nesneyi seçmek için)
    #
    # # x_Axis boyunca hareket
    # for i in range(X_AXIS):
    #     steppinx.write(1.0)
    #     steppinx.write(0.0)
    #
    # # Y_Axis boyunca hareket
    # for i in range(Y_AXIS):
    #     steppiny.write(1.0)
    #     steppiny.write(0.0)
    #     # time.sleep(0.0001)
    #
    # # geri dön
    # dirx.write(0.0)  # saat yönünün tersine (nesneyi bırakmak için)
    # diry.write(0.0)  # saat yönünün tersine (nesneyi bırakmak için)
    #
    # # Y_Axis boyunca hareket
    # for i in range(Y_AXIS):
    #     steppiny.write(1.0)
    #     # time.sleep(0.0001)
    #     steppiny.write(0.0)
    #     # time.sleep(0.0001)
    #
    # # x_Axis boyunca hareket
    # for i in range(X_AXIS):
    #     steppinx.write(1.0)
    #     # time.sleep(0.0001)
    #     steppinx.write(0.0)
    #     # time.sleep(0.0001)
    #
    # board.exit()
    # kapatmak için q ya bas
    k = cv2.waitKey(5)
    if k==ord("q"):
        break
        cv2.destroyAllWindows()
        cap.release()




