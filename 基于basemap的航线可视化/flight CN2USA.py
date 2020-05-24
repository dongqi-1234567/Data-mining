from pylab import mpl
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import matplotlib.lines as mlines
mpl.rcParams['font.sans-serif']=['KaiTi']
mpl.rcParams['axes.unicode_minus']=False


airport_col = ['ID', 'chufa', 'cflat', 'cflon','cftime', 'daoda', 'ddlon', 'ddlat', 'ddtime','cfnum', 'ddnum']
airport_df = pd.read_csv("E:\\data/all.csv",encoding = 'GB2312',names=airport_col)

route_cols = ['cfcity', 'cfsize', 'cflat', 'cflon','ddcity','ddsize', 'ddlat', 'ddlon']
routes_df = pd.read_csv("E:\\data/size.csv",encoding = 'GB2312',names=route_cols)

startnum=np.zeros((18,8),np.int)

fig=plt.figure(figsize = (8, 8))
# fig = plt.figure(figsize=(16,12))
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='ortho', lat_0=60, lon_0=-170,area_thresh=1000.0,ax = ax1)
map.bluemarble()
map.drawcoastlines()
map.drawcountries()
# map.fillcontinents(color = 'coral',alpha = .1)
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

#定义一个勾勒两点之间线段的函数：
def create_great_circles(df):
    for index,row in df.iterrows():
        start_lon = row['cflon']
        start_lat = row['cflat']
        end_lon = row['ddlon']
        end_lat = row['ddlat']
        #if abs(end_lat - start_lat) < 180 and abs(end_lon - start_lon) < 180:
        map.drawgreatcircle(start_lon, start_lat, end_lon, end_lat, linewidth=1,color = "lightsteelblue")
#执行航线绘制函数
create_great_circles(airport_df)




#定义一个填充散点图颜色、大小的函数
def create_start_points(df):
	lon   = np.array(df["cflon"])
	lat   = np.array(df["cflat"])
	pop   = np.array(df["cfsize"],dtype=float)
	x,y = map(lon,lat)
	for lon,lat,pop in zip(x,y,pop):
		map.scatter(lon,lat,marker="o",s=pop*50,color='royalblue')

#执行散点图填充函数
create_start_points(routes_df)

def create_end_points(df):
	lon   = np.array(df["ddlon"])
	lat   = np.array(df["ddlat"])
	pop   = np.array(df["ddsize"],dtype=float)
	x,y = map(lon,lat)
	for lon,lat,pop in zip(x,y,pop):
		map.scatter(lon,lat,marker = "o",s = pop*50,color = "royalblue")
#执行散点图填充函数
create_end_points(routes_df)
x, y = map(116.3, 39.9)
plt.text (x,y,'北京',rotation=-30,fontsize=30,color='lavender')
#保存图表
plt.savefig('E:ditu.jpg')#,dpi=1000,bbox_inches='tight')
plt.show()


