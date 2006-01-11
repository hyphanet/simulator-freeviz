import Image
import ImageDraw
import math
import handle
from nodes import nodes

nodes = handle.get_activenodes

im = Image.new('RGB',(800,800))
da = ImageDraw.Draw(im)
da.fill='red'


#big circle


#CENTER IS 220x220
#rad is 240
da.rectangle((0,0,im.size[0],im.size[1]),fill='white')
#da.chord((20,20,460,460),0,360, outline='red'   )
r = im.size[0]/2 - 20
u = 10

#for i in nodes:
for node in nodes:
	j =  node.location
	x = int(r * math.cos(j*2*math.pi))
	y = int(r * math.sin(j*2*math.pi))
	da.chord((x - 10 + im.size[0]/2, y-10 + im.size[1]/2,x+10+im.size[0]/2,y+10+im.size[1]/2),0,360,outline='red')


im.save('/tmp/ciclegraph.png','PNG')
