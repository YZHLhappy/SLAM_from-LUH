# coding: utf-8
#加入第一行是为了进行中文注释

#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）

# Plot the ticks from the left and right motor.
# 01_a_plot_motor_ticks.py
# Claus Brenner, 07 NOV 2012

#绘制左右电机的刻度线
# 01_a_plot_motor_ticks.py
#作者：# Claus Brenner, 07 NOV 2012


from pylab import *

if __name__ == '__main__':
    # Read all ticks of left and right motor.
    # Format is:
    # M timestamp[in ms] pos-left[in ticks] * * * pos-right[in ticks] ...
    # so we are interested in field 2 (left) and 6 (right).
    
    #读取左右电机对应的所有ticks信息
    #格式是：
    #M 时间戳[in ms] pos-left[in ticks] * * * pos-right[in ticks] ...
    #我们只需要第二列（左电机）和第六列（右电机）的数据
    
    f = open("robot4_motors.txt")    #打开robot4_motors.txt的数据
    left_list = []                   #建立名为left_list的数组
    right_list = []                  #建立名为right_list的数组
    for l in f:                      #对于l（行数）在f中（也就是所有在f中的数据走一遍）
        sp = l.split()               #每一个l代表一行数据，以行作为分割，然后将一行的数据赋予sp
        left_list.append(int(sp[2])) #sp[2]表示一行中第三个数据（0，1，2，所以2是第三个），此数据为左电机数据，append添加入left_list的数组
        right_list.append(int(sp[6]))#sp[6]表示一行中第7个数据，此数据为右电机数据，append添加入right_list数组中

    plot(left_list)                  #绘制左电机的数组在设定画布中的位置，定位y坐标，x坐标为l（行数）
    plot(right_list)                 #绘制右电机的数组在设定画布中的位置，定位y坐标，x坐标为l（行数）
    show()                           #左，右电机分别绘制出一个以l（行数）为x轴，left_list/right_list为y轴的图
