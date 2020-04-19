# coding: utf-8
#加入第一行是为了进行中文注释
#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）
#19.04.2020（复习）

# Compute the derivative of a scan.
# 03_b_scan_derivative
# Claus Brenner, 09 NOV 2012

#计算扫描数据的一阶导数值
#03_b_scan_derivative
#作者：Claus Brenner, 09 NOV 2012
from pylab import *
from lego_robot import *

# Find the derivative in scan data, ignoring invalid measurements.
#计算出扫描数据的一阶导数，并忽略无效数据（设置阈值来判断信息是否有效）
def compute_derivative(scan, min_dist):
    jumps = [ 0 ]
    for i in xrange(1, len(scan) - 1):
        # --->>> Insert your code here.
        # Compute derivative using formula "(f(i+1) - f(i-1)) / 2".
        # Do not use erroneous scan values, which are below min_dist.
        
        #在此输入你的代码
        #计算一阶导数用(f(i+1) - f(i-1)) / 2这个公式
        #不要使用错误的数据，这些数据低于min_dist值
        
        l=scan[i-1]                                           #（圆柱体的地标）的左边的扫描值l
        r=scan[i+1]                                           #（圆柱体的地标）的左边的扫描值r
        if(l > min_dist and r > min_dist):
            derivative=(r-l)/2.0
            jumps.append(derivative)
        else:
            jumps.append(0)
    jumps.append(0)        
    return jumps


if __name__ == '__main__':

    minimum_valid_distance = 20.0                             #最小有效距离=20.0

    # Read the logfile which contains all scans.读取包含所有扫描数据的文件
    logfile = LegoLogfile()                                   #将类LegoLogfile中的数据输如logfile
    logfile.read("robot4_scan.txt")                           #读取"robot4_scan.txt"的数据

    # Pick one scan.挑出一组扫描数据
    scan_no = 7
    scan = logfile.scan_data[scan_no]

    # Compute derivative, (-1, 0, 1) mask.计算导数（-1，0，1）掩码。
    der = compute_derivative(scan, minimum_valid_distance)

    # Plot scan and derivative.绘制出扫描数值和相应一阶导数值
    title("Plot of scan %d" % scan_no)
    plot(scan)
    plot(der)
    show()
