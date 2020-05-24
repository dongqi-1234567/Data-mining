import json
from datetime import datetime
import sys
import os
from tabulate import tabulate
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime, timezone
#from flightawareparser import fascrapper
#import flightawareparser
import urllib.request
import requests
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pylab import mpl


#获得飞行状态
def flightaware(flightnum):
    BASE = "https://flightaware.com/live/flight/"
    #HEADERS = ["time", "lat", "long", "alt", "gs"]
    #LIMIT = int(os.environ['LIMIT']) if 'LIMIT' in os.environ else 10

    if True:
        try:
            # flight = sys.argv[1].strip()
            flight = flightnum
            # print(flight)
        except:
            exit("请输入航班号！")

        try:
            response = requests.get(BASE + flight)
        except:
            exit("查询不到数据~请检查输入的航班号及是否联网！")

        #接收到301
        if response.status_code == 301:
            newurl = response.headers['Location']
            flight = newurl.split("/")[-1]
            response = requests.get(BASE + flight)

        # 从网页获得数据
        head = "<script>var trackpollBootstrap = "
        tail = ";</script>"

        for line in response.text.split("\n"):
            if head in line:
                data = line.replace(head, "").replace(tail, "")
                break

        tab = []
        try:
            data = json.loads(data)
        except:
            exit("Flight data not found")

        for key in data['flights']:
            flight_id = key
            break

        if "INVALID" in flight_id:
            exit("Invalid flight number")

        for track in data['flights'][flight_id]['track']:
            ts = int(track['timestamp'])
            timestamp = datetime.fromtimestamp(ts) \
                .strftime('%Y-%m-%d %H:%M:%S')
            row = [
                timestamp,
                track['coord'][0],
                track['coord'][1],
                track['alt'],
                track['gs']
            ]
            tab.append(row)
        # if len(tab) < LIMIT:
        #     print(tabulate(tab, headers=HEADERS))
        # else:

        #     print(tabulate(tab[-LIMIT:], headers=HEADERS))
        return tab

 #
from datetime import datetime, timezone
import json
import urllib.request
import requests
import re

class fascrapper:

    def __init__(self):
        self.urlbase = 'https://www.flightaware.com/live/'
        self.flightnum = ''
        self.aircrafttype = ''
        self.flightorg = ''
        self.flightdest = ''
        self.flightstatus = ''
        self.estgatedep = ''
        self.esttakeoff = ''
        self.estland = ''
        self.estgatearriv = ''
        self.actgatedep = ''
        self.acttakeoff = ''
        self.actland = ''
        self.actgatearriv = ''
        self.aircraftposition = ''
        self.alt = ''
        self.gspd = ''

    def gettime(self, epochtime):
        if epochtime != None and epochtime != []:
            gmttime = \
                datetime.utcfromtimestamp(epochtime).strftime('%B %d %Y %H:%M:%S'
                    )
        else:
            gmttime = epochtime
        return gmttime

    def faextract(self, flightno):
        faresponse = urllib.request.urlopen(self.urlbase + 'flight/'
                + flightno)
        fawebcontent = faresponse.read()
        fawebcontent = fawebcontent.decode('utf-8')
        faidx1 = fawebcontent.find('trackpollBootstrap = ')
        facontent = fawebcontent[faidx1 + 21:]
        faidx2 = facontent.find(';</script>')
        facontent = facontent[:faidx2]
        facontent.replace(';</script>', '', 1)
        facontent = facontent.strip()
        facontent = json.loads(facontent)
        return facontent

    def flightdata(self, flightcode):
        fldet = self.faextract(flightcode)
        flightkey = list(fldet['flights'].keys())
        self.flightnum = fldet['flights'][flightkey[0]]['friendlyIdent']
        self.flightstatus = fldet['flights'
                                  ][flightkey[0]]['flightStatus']
        self.aircrafttype = fldet['flights'][flightkey[0]]['aircraft'
                ]['friendlyType']
        self.flightorg = fldet['flights'][flightkey[0]]['origin'
                ]['friendlyLocation']
        self.flightdest = fldet['flights'][flightkey[0]]['destination'
                ]['friendlyLocation']
        self.estgatedep = fldet['flights'
                                ][flightkey[0]]['gateDepartureTimes'
                ]['estimated']
        self.esttakeoff = fldet['flights'][flightkey[0]]['takeoffTimes'
                ]['estimated']
        self.estland = fldet['flights'][flightkey[0]]['landingTimes'
                ]['estimated']
        self.estgatearriv = fldet['flights'
                                  ][flightkey[0]]['gateArrivalTimes'
                ]['estimated']
        self.estgatedep = self.gettime(fldet['flights'
                ][flightkey[0]]['gateDepartureTimes']['estimated'])
        self.esttakeoff = self.gettime(fldet['flights'
                ][flightkey[0]]['takeoffTimes']['estimated'])
        self.estland = self.gettime(fldet['flights'
                                    ][flightkey[0]]['landingTimes'
                                    ]['estimated'])
        self.estgatearriv = self.gettime(fldet['flights'
                ][flightkey[0]]['gateArrivalTimes']['estimated'])
        self.actgatedep = self.gettime(fldet['flights'
                ][flightkey[0]]['gateDepartureTimes']['actual'])
        self.acttakeoff = self.gettime(fldet['flights'
                ][flightkey[0]]['takeoffTimes']['actual'])
        self.actland = self.gettime(fldet['flights'
                                    ][flightkey[0]]['landingTimes'
                                    ]['actual'])
        self.actgatearriv = self.gettime(fldet['flights'
                ][flightkey[0]]['gateArrivalTimes']['actual'])
        self.alt = fldet['flights'][flightkey[0]]['altitude']
        self.gspd = fldet['flights'][flightkey[0]]['groundspeed']
        if self.flightstatus == 'airborne':
            if self.actgatedep == None:
                self.distcov = ''
                self.distrem = ''
                self.aircraftposition = 'Unkown'
            elif self.actgatedep != None and self.acttakeoff == None:
                self.distcov = ''
                self.distrem = ''
                self.aircraftposition = \
                    'Departed gate. Taxiing for takeoff'
            elif self.actgatedep != None and self.acttakeoff != None:
                self.distcov = fldet['flights'][flightkey[0]]['distance'
                        ]['elapsed']
                self.distrem = fldet['flights'][flightkey[0]]['distance'
                        ]['remaining']
                self.aircraftposition = 'In air, covered ' \
                    + str(self.distcov) + ' nautical miles with ' \
                    + str(self.distrem) + ' nautical miles remaining.'
        elif self.flightstatus == 'arrived':
            if self.actland == None:
                self.aircraftposition = 'Unkown'
            elif self.actland != None and self.actgatearriv == None:
                self.aircraftposition = \
                    'Arrived at destination. Taxiing to gate'
            elif self.actland != None and self.actgatearriv != None:
                self.aircraftposition = \
                    'Arrived at destination and at the gate'
            else:
                self.aircraftposition = 'Unkown'
        elif self.flightstatus == None or self.flightstatus == '':
            self.aircraftposition = 'Unkown'
        else:
            self.aircraftposition = 'Unkown'
        return (
            self.flightnum,
            self.aircrafttype,
            self.flightorg,
            self.flightdest,
            self.flightstatus,
            self.alt,
            self.gspd,
            self.estgatedep,
            self.esttakeoff,
            self.estland,
            self.estgatearriv,
            self.actgatedep,
            self.acttakeoff,
            self.actland,
            self.actgatearriv,
            self.aircraftposition,
            )
#

#画图函数
mpl.rcParams['font.sans-serif']=['KaiTi']
mpl.rcParams['axes.unicode_minus']=False
def image_result(flightnum):
    #设置画布大小
    plt.figure(figsize=(8,8))
    #画一幅中国地图
    map1 = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51)
    # map1 = Basemap(resolution = 'h' , llcrnrlon=73, llcrnrlat=18, urcrnrlon=135, urcrnrlat=53)
    #画出国家边界
    map1.drawcountries()
    #画出海岸线
    # map1.drawcoastlines()
    #画一幅NASA的bluemarble地图
    map1.bluemarble()
    #获取航班信息
    flight = flightaware(flightnum)
    #获得航班总共的信息条数
    z = len(flight)
    #导入函数
   # facheck= flightawareparser.fascrapper()
    facheck = fascrapper()
    #获得航班号对应的航班起始站点的信息
    details=facheck.flightdata(flightnum)
    #取整条航线上的四个点
    x1,y1 = map1(flight[1][1],flight[1][2])
    x2,y2 = map1(flight[int(z/3)][1],flight[int(z/3)][2])
    x3,y3 = map1(flight[int(2*z/3)][1],flight[int(2*z/3)][2])
    x4,y4 = map1(flight[z - 1][1],flight[z - 1][2])
    x = [x1,x2,x3,x4]
    y = [y1,y2,y3,y4]
    #画点
    map1.scatter(x,y,270,marker = 'o',color = 'steelblue')
    #画线
    map1.drawgreatcircle(x1,y1,x2,y2,linewidth=2,color = 'lightblue')
    map1.drawgreatcircle(x2,y2,x3,y3,linewidth=2,color = 'lightblue')
    map1.drawgreatcircle(x3,y3,x4,y4,linewidth=2,color = 'lightblue')
    #备注文字
    plt.text(x1,y1,flight[1][0],rotation=0,fontsize=10,color = 'lawngreen')
    plt.text(x1,y1,details[2],rotation=30,fontsize=12,color = 'snow')
    plt.text(x2,y2,flight[int(z/3)][0],rotation=0,fontsize=10,color = 'lawngreen')
    plt.text(x3,y3,flight[int(2*z/3)][0],rotation=0,fontsize=10,color = 'lawngreen')
    plt.text(x4,y4,flight[z - 1][0],rotation=0,fontsize=10,color = 'lawngreen')
    plt.text(x4,y4,details[3],rotation=30,fontsize=12,color = 'snow')
    #plt.text(x2, y2, '北京', rotation=30, fontsize=15, color='coral')
    plt.savefig('flight.png')
    # plt.show()


# image_result('CSN3437')
import tkinter
import pygeoip
#from flightawareimage import *
from PIL import Image, ImageTk
from tabulate import tabulate


class FindLight(object):
    global img_png
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容及大小
        self.root.title("请输入航班号")
        self.root.geometry('600x600')

        # 创建一个输入框,并设置尺寸
        self.ip_input = tkinter.Entry(self.root, width=1000)

        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root, width=1000)
        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command=self.find_flight, text="查询")

    # 完成布局
    def gui_arrang(self):
        self.ip_input.pack()
        self.display_info.pack()
        self.result_button.pack()

    # 根据ip查找地理位置
    def find_flight(self):
        # 获取输入信息
        self.fight_num = self.ip_input.get()
        the_ip_info=flightaware(str(self.fight_num))

        print(the_ip_info)

        for item in range(100):
            self.display_info.insert(0, "")

        #为回显列表赋值
        for item in the_ip_info:
            self.display_info.insert(0, item)
        #这里的返回值,没啥用,就是为了好看
        return the_ip_info

    def Open_Img(self):
        global img_png
        image_result(self.fight_num)
        Img = Image.open('flight.png')
        img_png = ImageTk.PhotoImage(Img)
        label_Img = tkinter.Label(self.root, image=img_png,width=1000,height=1000)
        label_Img.pack()

    def btn_pic(self):
        btn_Open = tkinter.Button(self.root,
                         text='打开图像',  # 显示在按钮上的文字
                         width=15, height=2,
                         command=self.Open_Img)  # 点击按钮式执行的命令
        btn_Open.pack()  # 按钮位置

def main():
    # 初始化对象
    FL = FindLight()
    # 进行布局
    FL.gui_arrang()
    # 主程序执行
    FL.btn_pic()
    tkinter.mainloop()

    pass


if __name__ == "__main__":
    main()
