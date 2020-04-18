# coding: utf-8
#加入第一行是为了进行中文注释

#YZHL学习并尝试翻译（以下翻译仅为了自行学习方便）

# Python routines useful for handling ikg's LEGO robot data.
# Author: Claus Brenner, 28.10.2012

#Python的例行程序用于处理ikg的乐高机器人数据
#作者：Claus Brenner， 28.10.2012


# In previous versions, the S record included the number of scan points.
# If so, set this to true.
#在以前的版本中，S记录包含扫描点的数量。
#如果是这样，请将其设置为true。

s_record_has_count = True

# Class holding log data of our Lego robot.
# The logfile understands the following records:
# P reference position (of the robot)
# S scan data
# I indices of poles in the scan data (determined by an external algorithm)
# M motor (ticks from the odometer) data
# F filtered data (robot position, or position and heading angle)
# L landmark (reference landmark, fixed)
# D detected landmark, in the scanner's coordinate system

#Class包含我们的乐高机器人的日志数据
#logfile的标记含义如下
#P 表示机器人的位置
#S 扫描数据
#I 在扫描数据中的极点的索引（由外部算法确定）
#M motor的数据（里程表上的刻度）
#F 过滤后的数据（机器人的位置，或者位置，和方位角/航向角）
#L Landmark（地标）（参考地表，且是固定的）
#D 发现的Landmark，在扫描数据下的坐标系系统中


#自我理解的Legofile（object）运行原理记录
#首先定义LegoLogfile(object)为一个类，
#然后定义类的实例用__init__（self），在其中（__init__（self））定义了所需要的数据数组
#紧接着定义了read（）函数，作用为读取文件数据，其中包含P,M,S等数据读取方式（作者规定的方式），例如：M的读取（M.txt的read）
#下面以M的读取（M.txt的read）为例子进行说明：
#第一步进入class LegoLogfile(object)，然后执行第一个def __init__(self)中的内容，此时获取了p，s，m等新建空数组，然后执行.read("robot4_motors.txt")后，
#进入到read，之后通过open（）将文件打开，然后用sp=l.split()将数据分行（l代表每一个在f中的数据，换言之就是遍历一遍所有文件数据），
#为什么说l.split（）可以分行，因为设置好的数据的存储方式是每一行的第一个为M（其他数据为S，P等），
#所以每读取到每行第一个，也就是sp[0]时，将会通过对sp[0]=什么来判断读取的数据为P还是S还是M等，此例子为M，所以以M继续分析，
#进入到M后，ticks = (int(sp[2]), int(sp[6]))表示用ticks（，）分别记录了左右电机的数据（存储认为设定：sp[2]为左，sp[6]为右，所以可写为ticks（左，右）
#然后if first_motor_ticks:，对应前面的first_motor_ticks = True，也就是可以进入if语句中，然后self.motor_ticks = []表示设定一个空数组；
#然后first_motor_ticks = False是为了这次if只执行一次，
#然后self.last_ticks = ticks，也就是将ticks（左，右）的值赋予self.last_ticks
#然后self.motor_ticks.append(tuple([ticks[i]-self.last_ticks[i] for i in range(2)]))以及self.last_ticks = ticks，表示，需要将ticks[0到1]-sel.last_tick[0到1]算出来并添加到self.motor_ticks数组中，
#此处需要说明，ticks[0]表示ticks(左，右)的左，因为ticks是一个数组，0表示数组中第一个数，ticks[1]代表右，换言之，这个操作就是为了得出左/右电机t时刻的数据和t-1时刻数据的差值，以此来计算变化量


class LegoLogfile(object):                     #创建一个名为“LegoLogfile”的类
    def __init__(self):                        #__init__（）类的构造函数或初始化方法
        self.reference_positions = []          #self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数
        self.scan_data = []
        self.pole_indices = []
        self.motor_ticks = []
        self.filtered_positions = []
        self.landmarks = []
        self.detected_cylinders = []
        self.last_ticks = None

    def read(self, filename):
        """Reads log data from file. Calling this multiple times with different
           files will result in a merge of the data, i.e. if one file contains
           M and S data, and the other contains M and P data, then LegoLogfile
           will contain S from the first file and M and P from the second file."""
           
        """读取日志数据从文件中。访问多次不同的文件将会得到数据合并，例如:如果一个文件包含
            M和S数据，另一个文件包含M和P数据，之后LegoLogefile将会包含从第一个文件中提取的S数据，
            M和P数据将会从第二个文件中读取"""
        # If information is read in repeatedly, replace the lists instead of appending,
        # but only replace those lists that are present in the data.
        
        #如果信息要重复读取，替换列表而不是去附加列表，
        #但是仅仅要替代那些存在与数据中的列表（注：存疑）
        first_reference_positions = True
        first_scan_data = True
        first_pole_indices = True
        first_motor_ticks = True
        first_filtered_positions = True
        first_landmarks = True
        first_detected_cylinders = True
        f = open(filename)
        for l in f:
            sp = l.split()
            # P is the reference position.
            # File format: P timestamp[in ms] x[in mm] y[in mm]
            # Stored: A list of tuples [(x, y), ...] in reference_positions.
            
            #P 是参考位置
            #文件格式：P 时间戳记[in ms]  x[in mm]  y[in mm] (注：x，y为坐标值)
            if sp[0] == 'P':
                if first_reference_positions:
                    self.reference_positions = []
                    first_reference_positions = False 
                self.reference_positions.append( (int(sp[2]), int(sp[3])) )

            # S is the scan data.
            # File format:
            #  S timestamp[in ms] distances[in mm] ...
            # Or, in previous versions (set s_record_has_count to True):
            #  S timestamp[in ms] count distances[in mm] ...
            # Stored: A list of tuples [ [(scan1_distance,... ), (scan2_distance,...) ]
            #   containing all scans, in scan_data.
            
            #S 是扫描数据
            #文件格式：
            #S 时间戳记[in ms]  距离[in mm]...
            #或者，在先前的版本中（将s_record_has_count 为“true”）
            #S 时间戳记[in ms]  距离[in mm]...
            #已存储：A 元组列表[ [(scan1_distance,...),(sanc2_distance,...)]]
            #在scan_data中包含所有扫描数据
            elif sp[0] == 'S':
                if first_scan_data:
                    self.scan_data = []
                    first_scan_data = False
                if s_record_has_count:
                    self.scan_data.append(tuple(map(int, sp[3:])))
                else:
                    self.scan_data.append(tuple(map(int, sp[2:])))

            # I is indices of poles in the scan.
            # The indices are given in scan order (counterclockwise).
            # -1 means that the pole could not be clearly detected.
            # File format: I timestamp[in ms] index ...
            # Stored: A list of tuples of indices (including empty tuples):
            #  [(scan1_pole1, scan1_pole2,...), (scan2_pole1,...)...]
            
            #I 是indices of poles 在扫描数据中
            #索引以扫描顺序给出（逆时针）
            #-1表示无法清楚地检测到poles。
            #已存储：A 索引元组列表（包括空元组）
            #  [(scan1_pole1, scan1_pole2,...), (scan2_pole1,...)...]
            
            elif sp[0] == 'I':
                if first_pole_indices:
                    self.pole_indices = []
                    first_pole_indices = False
                self.pole_indices.append(tuple(map(int, sp[2:])))

            # M is the motor data.
            # File format: M timestamp[in ms] pos[in ticks] tachoCount[in ticks] acceleration[deg/s^2] rotationSpeed[deg/s] ...
            #   (4 values each for: left motor, right motor, and third motor (not used)).
            # Stored: A list of tuples [ (inc-left, inc-right), ... ] with tick increments, in motor_ticks.
            # Note that the file contains absolute ticks, but motor_ticks contains the increments (differences).
            
            #M 是电机的数据
            #文件格式：M 时间戳[in ms]，pos[in ticks]，转速计tachoCount[in ticks]，加速度[deg / s ^ 2]，旋转速度[deg/s] ...
            #（4个值分别为：左电机，右电机和第三个电机（未使用））
            elif sp[0] == 'M':
                ticks = (int(sp[2]), int(sp[6]))
                if first_motor_ticks:
                    self.motor_ticks = []
                    first_motor_ticks = False
                    self.last_ticks = ticks
                self.motor_ticks.append(
                    tuple([ticks[i]-self.last_ticks[i] for i in range(2)]))
                self.last_ticks = ticks

            # F is filtered trajectory. No time stamp is used.
            # File format: F x[in mm] y[in mm]
            # OR:          F x[in mm] y[in mm] heading[in radians]
            # Stored: A list of tuples, each tuple is (x y) or (x y heading)
            
            #F 是过滤后的轨迹，不使用时间戳
            #文件格式：F,  x[in mm]， y[in mm]
            #或者： F,  x[in mm],  y[in mm],  heading[in radians]
            elif sp[0] == 'F':
                if first_filtered_positions:
                    self.filtered_positions = []
                    first_filtered_positions = False
                self.filtered_positions.append( tuple( map(float, sp[1:])) )

            # L is landmark. This is actually background information, independent
            # of time.
            # File format: L <type> info...
            # Supported types:
            # Cylinder: L C x y diameter.
            # Stored: List of (<type> info) tuples.
            #Cylinder: L C x y diameter
            
            #L是地标（一个固定的物体）。实际上就是背景信息，不随时间变化
            #文件格式：L <type> info...
            #支持的类型：
            #Cylinder: L C x y diameter  （圆柱体，L,C,x,y,直径）
            elif sp[0] == 'L':
                if first_landmarks:
                    self.landmarks = []
                    first_landmarks = False
                if sp[1] == 'C':
                    self.landmarks.append( tuple(['C'] + map(float, sp[2:])) )
                    
            # D is detected landmarks (in each scan).
            # File format: D <type> info...
            # Supported types:
            # Cylinder: D C x y x y ...
            # Stored: List of lists of (x, y) tuples of the cylinder positions,
            #  one list per scan.
            
            #D是发现的地标（在每次扫描中）
            #文件格式：D <type> info...
            #支持的类型：
            #Cylinder: D C x y x y ...
            #存储方式：(x,y) 圆柱体位置的元数据列表的列表
            #一次扫描生成一个列表
            elif sp[0] == 'D':
                if sp[1] == 'C':
                    if first_detected_cylinders:
                        self.detected_cylinders = []
                        first_detected_cylinders = False
                    cyl = map(float, sp[2:])
                    self.detected_cylinders.append([(cyl[2*i], cyl[2*i+1]) for i in range(len(cyl)/2)])

        f.close()

    def size(self):
        """Return the number of entries. Take the max, since some lists may be empty."""
        return max(len(self.reference_positions), len(self.scan_data),
                   len(self.pole_indices), len(self.motor_ticks),
                   len(self.filtered_positions), len(self.detected_cylinders))

    @staticmethod
    def beam_index_to_angle(i, mounting_angle = -0.06981317007977318):
        """Convert a beam index to an angle, in radians."""
        return (i - 330.0) * 0.006135923151543 + mounting_angle

    def info(self, i):
        """Prints reference pos, number of scan points, and motor ticks."""
        s = ""
        if i < len(self.reference_positions):
            s += " | ref-pos: %4d %4d" % self.reference_positions[i]

        if i < len(self.scan_data):
            s += " | scan-points: %d" % len(self.scan_data[i])

        if i < len(self.pole_indices):
            indices = self.pole_indices[i]
            if indices:
                s += " | pole-indices:"
                for idx in indices:
                    s += " %d" % idx
            else:
                s += " | (no pole indices)"
                    
        if i < len(self.motor_ticks):
            s += " | motor: %d %d" % self.motor_ticks[i]

        if i < len(self.filtered_positions):
            f = self.filtered_positions[i]
            s += " | filtered-pos:"
            for j in range(len(f)):
                s += " %.1f" % f[j]

        return s
