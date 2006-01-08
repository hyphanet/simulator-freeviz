#!/usr/bin/env python

precision=10

import gdchart
from math import floor
import sys
sys.path+=['/home/sleon/public_html/bla/']

import histdata
	


def gen(trans):
	links = histdata.get(trans)
	chunk=0.5 / float(precision)

	histogram=[]
	for x in range(0,precision):
		 histogram.append(0)
	number_of_connections=len(links)
	if number_of_connections == 0:
		return
	
	#print "They are "+str(number_of_connections)+" connections."
	
	for connection in links:
		a = float(connection[0].get("location"))
		b = float(connection[1].get("location"))
		#a number between 0 and 0.5
		delta = min(abs(a-b), 1-abs(a-b))
		
		index=0
		for i in range(precision):
			if chunk * float(i) <= delta and chunk * float(i+1) > delta:
				index = i
				break
			
		histogram[index]=histogram[index]+1
	
	histogram_percents=[ (x*100)/number_of_connections for x in histogram ]
	
	x = gdchart.Bar3D()
	x.width = 250
	x.height = 250
	x.xtitle = "Distance"
	x.ytitle = "%"
	x.title = "Histogram of link location distances"
	x.ext_color = [ 0x055202 , 0x169310 , 0x298760 , 0x297987 , 0xc1d72b , 0xd4f113 , 0xf18113 , 0xf13713 , 0xcf0000 , 0x700606 ]
	x.setData(histogram_percents)
	label=[]
	for i in range(0,precision):
		column_name = str(chunk * i)
		label.append(column_name)
	x.setLabels(label)
	x.draw("/tmp/histogram.png")
	#print histogram
	#print histogram_percents
