#!/usr/bin/env python

precision=10

import gdchart
from math import floor
import sys
sys.path+=['/home/sleon/public_html/bla/']

import histdata
	


def gen():
	links = histdata.get()

	histogram=[]
	for x in range(0,precision):
		 histogram.append(0)
	number_of_connections=len(links)
	
	#print "They are "+str(number_of_connections)+" connections."
	
	for connection in links:
		delta=float(connection[0].get("location"))-float(connection[1].get("location"))
		index=int(floor(abs(delta*precision)))
		histogram[index]=histogram[index]+1
	
	histogram_percents=[ (x*100)/number_of_connections for x in histogram ]
	
	x = gdchart.Bar3D()
	x.width = 250
	x.height = 250
	x.xtitle = "Distance"
	x.ytitle = "%"
	x.title = "Histogram of link location distances"
	x.ext_color = [ 0x055202 , 0x169310 , 0x298760 , 0x297987 , 0xc1d72b , 0xd4f113 , 0xf18113 , 0xf13713 , 0xcf0000 , 0x000000 ]
	x.setData(histogram_percents)
	label=[]
	for column_name in range(0,precision):
		 label.append(str(column_name))
	x.setLabels(label)
	x.draw("/tmp/histogram.png")
	#print histogram
	#print histogram_percents
