# coding: utf-8
#加入第一行是为了进行中文注释
#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）
#19.04.2020（复习）

# Implement the second move model for the Lego robot.
# The difference to the first implementation is:
# - added a scanner displacement
# - added a different start pose (measured in the real world)
# - result is now output to a file, as "F" ("filtered") records.
#
#给lego机器人编写第二个运动模型
#与第一个模型不同的是：
#- 添加了一个扫描传感器的偏移距离（因为传感器不在机器人中心，所以要算出偏移距离）
#- 添加了不同的开商点（在真实世界中测量）
#- 现在的结果输出到一个文件，作为F（过滤的值）记录

# 02_b_filter_motor_file
#Claus Brenner, 09 NOV 2012
# 作者：Claus Brenner, 09 NOV 2012
from math import sin, cos, pi
from lego_robot import *

# This function takes the old (x, y, heading) pose and the motor ticks
# (ticks_left, ticks_right) and returns the new (x, y, heading).
#这个函数输入旧的/上一时刻的(x, y, heading) 姿态（位置与方向），并返回输出新的(x, y, heading)
def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width,
                scanner_displacement):
    l=motor_ticks[0]*ticks_to_mm
    r=motor_ticks[1]*ticks_to_mm
    
    x=pose[0]  #x的值为上一时刻的pose的index0的值
    y=pose[1]  #y的值为上一时刻的pose的index1的值
    # Find out if there is a turn at all.判断是否有转弯
    if motor_ticks[0] == motor_ticks[1]:
        # No turn. Just drive straight.如果没有转弯，则为行驶直线  

        # --->>> Use your previous implementation.使用之前的程序
        # Think about if you need to modify your old code due to the
        # scanner displacement?思考是否需要新建一个运动模型来应对增加的扫描仪距离中心的距离差？ 答，直线时不需要
        theta=pose[2]  #theta的值为上一时刻的pose的index3的值
        x=x+l*cos(theta)  #新的x值
        y=y+r*sin(theta)  #新的y值
        
        return (x, y, theta)

    else:
        # Turn. Compute alpha, R, etc.

        # --->>> Modify your previous implementation.建立在之前的模型上
        w=robot_width  #机器人的宽赋值给w，方便书写
        theta_old=pose[2]
        
        alpha=(r-l)/w  #计算出转弯的角度增量alpha
        R=l/alpha      #计算出转弯半径
        # First modify the the old pose to get the center (because the
        # old pose is the LiDAR's pose, not the robot's center pose).首先由于第一个模型的pose建立在robot的中心，而lidar不在中心，所以需要重新建模
        x=x-scanner_displacement * cos(theta_old)
        y=y-scanner_displacement * sin(theta_old)
        
        # Second, execute your old code, which implements the motion model
        # for the center of the robot.其次，执行您的旧代码，该代码实现了机器人中心的运动模型
        theta=(theta_old+alpha)%(2*pi)  #新的theta值=旧的+alpha，后面的（%2*pi）是为了防止出现角度的其他值，因为三角函数为周期函数
        cx=x+(R+w/2)*sin((theta)-sin(theta_old))
        cy=y+(R+w/2)*(-cos(theta)+cos(theta_old))
        # Third, modify the result to get back the LiDAR pose from
        # your computed center. This is the value you have to return.第三，获得lidar的姿态（位置和方向）与计算中心的转换        
        x = cx+scanner_displacement*cos(theta)  #新x的值
        y = cy + scanner_displacement*sin(theta)  #新y的值
        
        return (x, y, theta)

if __name__ == '__main__':
    # Empirically derived distance between scanner and assumed根据经验得出的扫描仪与假定位置之间的距离
    # center of robot.机器人的中心位置
    scanner_displacement = 30.0

    # Empirically derived conversion from ticks to mm.根据经验得出的转化从ticks到mm（也就是一个单位的tick等于0.349mm）
    ticks_to_mm = 0.349 

    # Measured width of the robot (wheel gauge), in mm.测量机器人的宽（轮间距），单位为mm
    robot_width = 150.0

    # Measured start position.测量到的起始位置
    pose = (1850.0, 1897.0, 213.0 / 180.0 * pi)

    # Read data.读取数据
    logfile = LegoLogfile()
    logfile.read("robot4_motors.txt")

    # Loop over all motor tick records generate filtered position list.#循环所有的电机tick的记录生成过滤后的位置列表
    filtered = []
    for ticks in logfile.motor_ticks:
        pose = filter_step(pose, ticks, ticks_to_mm, robot_width,
                           scanner_displacement)
        filtered.append(pose)

    # Write all filtered positions to file.将所有获得滤波值写入文件
    f = open("poses_from_ticks.txt", "w")
    for pose in filtered:
        print >> f, "F %f %f %f" % pose
    f.close()
