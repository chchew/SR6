from bmp import *
from obj import *
from math import *
from collections import namedtuple



def renderer():
	renderer = Bitmap(1200,1200)
	tex = Texture('./modelos/goku.bmp')
	renderer.load('./modelos/goku.obj', mtlFile=None, translate=(0.1,-0.5,0), scale=(2,2,2), rotate=(0.2,-0.3,0), ojo=V3(0,-0.2,1), arriba=V3(0,1,0), centro=V3(0,0,0), texture=tex)
	renderer.archivo('goku.bmp')

renderer()
