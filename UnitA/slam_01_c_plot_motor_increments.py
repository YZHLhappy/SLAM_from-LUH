# coding: utf-8
#加入第一行是为了进行中文注释

#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）
#19.04.2020（复习）

# Plot the increments of the left and right motor.
# 01_c_plot_motor_increments.py
# Claus Brenner, 07 NOV 2012

#绘制左右电机的增量值
#01_c_plot_motor_increments.py
#作者：# Claus Brenner, 07 NOV 2012

from pylab import *                     #因为要用到plot()，所以要引入pylab
from lego_robot import LegoLogfile      #引入类LegoLogfile从lego_robot中

if __name__ == '__main__':

    logfile = LegoLogfile()             #将LegoLogfile()赋值给logfile
    logfile.read("robot4_motors.txt")   #读取robot4_motors.txt，获得self.motor_ticks值，此值为左右电机的增量

    plot(logfile.motor_ticks)           #绘制左右电机增量的值，横坐标为M数据的行号，纵坐标为增量
    show()
    
    
    
    
#如何输出仅一个电机的数据
#思考：logfile.motor_ticks是一个nx2的数组，那么我只想读取第一列
#    for i in range(10,30):
#        a=[]
#        a.append(tuple(logfile.motor_ticks[i]))
 #       print a[i,0]
#        for j in range(10):
#            b=[]
#            b.append(a[0])
#            print b
           

