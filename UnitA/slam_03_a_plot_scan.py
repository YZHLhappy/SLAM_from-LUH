# coding: utf-8
#加入第一行是为了进行中文注释
#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）
#19.04.2020（复习）

# Plot a scan of the robot using matplotlib.
# 03_a_plot_scan
# Claus Brenner, 09 NOV 2012
#用matplotlib绘制机器人扫描结果
#03_a_plot_scan
#作者：Claus Brenner, 09 NOV 2012
from pylab import *
from lego_robot import *

# Read the logfile which contains all scans.
#读取包含所有扫面数据的文件
logfile = LegoLogfile()
logfile.read("robot4_scan.txt")

# Plot one scan.
#绘制一个扫描结果
plot(logfile.scan_data[8])
show()
