# coding: utf-8
#加入第一行是为了进行中文注释

#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）

# Print the increments of the left and right motor.
# Now using the LegoLogfile class.
# 01_b_print_motor_increments.py
# Claus Brenner, 07 NOV 2012

#输出/显示 左右电机数据的增量
#现在使用类“LegoLogfile”
# 01_b_print_motor_increments.py
# 作者：Claus Brenner, 07 NOV 2012
from lego_robot import LegoLogfile  #从lego_robot文件中输入类LegoLogfile

if __name__ == '__main__':

    logfile = LegoLogfile()  #将类LegoLogfile的值赋予logfile
    logfile.read("robot4_motors.txt")  #logfile使用.readrobot4.motors.txt的M行开头进入到“elif sp[0] == 'M':”

    for i in range(0,200):  #从0到199
        print logfile.motor_ticks[i]  #输出对应的差值数据

