#!/usr/bin/env python

try:
	import gdchart
	from math import floor
	import histdata
	
	links = histdata.get()
except:
	print "Blame sleon if his api is b0rk3d! :p"
	quit

histogram=[0,0,0,0,0,0,0,0,0,0]
number_of_connections=len(links)

print "They are "+str(number_of_connections)+" connections."

for connection in links:
	delta=float(connection[0].get("location"))-float(connection[1].get("location"))
	index=int(floor(abs(delta*10)))
	histogram[index]=histogram[index]+1

histogram_percents=[ (x*100)/number_of_connections for x in histogram ]

x = gdchart.Bar3D()
x.width = 250
x.height = 250
x.xtitle = "Distance"
x.ytitle = "Percentage"
x.title = "Histogram of link location distances"
x.ext_color = [ 0x055202 , 0x169310 , 0x298760 , 0x297987 , 0xc1d72b , 0xd4f113 , 0xf18113 , 0xf13713 , 0xcf0000 , 0x000000 ]
x.setData(histogram_percents)
x.setLabels(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
x.draw("histogram.png")
print histogram
print histogram_percents
