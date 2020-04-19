# coding: utf-8
#加入第一行是为了进行中文注释

#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）
#19.04.2020（复习）

# Implement the first move model for the Lego robot.
# 02_a_filter_motor
# Claus Brenner, 31 OCT 2012

#编写第一个lego机器人的移动模型
#02_a_filter_motor
#作者：Claus Brenner, 31 OCT 2012

from math import sin, cos, pi
from pylab import *
from lego_robot import *

# This function takes the old (x, y, heading) pose and the motor ticks
# (ticks_left, ticks_right) and returns the new (x, y, heading).

#这个函数输入old (x, y, heading)的姿态（位置和方向）和电机ticks（左，右），并输出新的 (x, y, heading)
def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width):
    l=motor_ticks[0]*ticks_to_mm
    r=motor_ticks[1]*ticks_to_mm
    # Find out if there is a turn at all.判断是否有转弯
    if motor_ticks[0] == motor_ticks[1]:
        # No turn. Just drive straight. 如果没有转弯，则为行驶直线  
        # --->>> Implement your code to compute x, y, theta here.
        x=pose[0]  #x的值为上一时刻的pose的index0的值
        y=pose[1]  #y的值为上一时刻的pose的index1的值
        theta=pose[2]  #theta的值为上一时刻的pose的index3的值
        
        x=x+l*cos(theta)  #新的x值
        y=y+r*sin(theta)  #新的y值
        
        return (x, y, theta)  #输出新（x,y,theta)

    else:
        # Turn. Compute alpha, R, etc.如果转弯，则要算出alpha角度变化量，R转弯半径（从机器人中轴线到左电机/轮）等参数
        # --->>> Implement your code to compute x, y, theta here.
        x=pose[0]  #x的值为上一时刻的pose的index0的值
        y=pose[1]  #y的值为上一时刻的pose的index1的值
        theta=pose[2]  #theta的值为上一时刻的pose的index3的值
        
        w=robot_width  #机器人的宽赋值给w，方便书写
        
        alpha=(r-l)/w  #计算出转弯的角度增量alpha
        R=l/alpha      #计算出转弯半径
        cx=x-(R+w/2)*sin(theta)  #转弯中心点的x坐标，以机器人的pose为坐标系原点
        cy=y+(R+w/2)*cos(theta)  #转弯中心点的y坐标，以机器人的pose为坐标系原点
        
        theta=(theta+alpha)%(2*pi)  #新的theta值=旧的+alpha，后面的（%2*pi）是为了防止出现角度的其他值，因为三角函数为周期函数
        x=cx+(R+w/2)*sin(theta)  #新x的值
        y=cy-(R+w/2)*cos(theta)  #新y的值
        
        return(x,y,theta)  #输出新（x,y,theta)

if __name__ == '__main__':
    # Empirically derived conversion from ticks to mm.
    #根据经验得出的转化从ticks到mm（也就是一个单位的tick等于0.349mm）
    ticks_to_mm = 0.349  #一个tick等于0.349mm，这个值是此模型的，根据模型不同会有相应变化

    # Measured width of the robot (wheel gauge), in mm.
    #测量机器人的宽（轮间距），单位为mm
    robot_width = 150.0  #机器人宽为150.0mm

    # Read data.
    #读取数据
    logfile = LegoLogfile()
    logfile.read("robot4_motors.txt")  #得到legofile.motor_ticks的数据，一个此数据为一个时刻的左右电机数据

    # Start at origin (0,0), looking along x axis (alpha = 0).
    #开始点在原点（0，0），方向角为0°，朝向为x轴
    pose = (0.0, 0.0, 0.0)  #pose代表机器人的位置，此时x=0，y=0，方向角=0°

    # Loop over all motor tick records generate filtered position list.
    #循环所有的电机tick的记录生成过滤后的位置列表
    filtered = []  #设立一个数组
    for ticks in logfile.motor_ticks:  #对每个ticks进行一次遍历
        pose = filter_step(pose, ticks, ticks_to_mm, robot_width)  #用前面自己书写的模型函数，计算出机器人的pose（x,y,theta)，这个模型函数，输入为4个参数，输出三个
        filtered.append(pose)  #将每一个pose加入filtered数组中

    # Draw result.
    #绘制结果
    for pose in filtered:  #对所有在filtered中的pose进行遍历
        print pose         #打印输出每一个pose
        plot([p[0] for p in filtered], [p[1] for p in filtered], 'bo')  #绘制
    show()
