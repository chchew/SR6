import struct
from obj import *
from math import *
from math import sin, cos

from collections import namedtuple

V2 = namedtuple('Punto2', ['x', 'y'])
V3 = namedtuple('Punto3', ['x', 'y', 'z'])

def char(c):
	return struct.pack("=c",c.encode('ascii'))

def word(c):
	return struct.pack("=h",c)

def dword(c):
	return struct.pack("=l",c)

def color(r,g,b):
	return bytes([b,g,r])

def sum(v0,v1):

	px = v0.x + v1.x
	py = v0.y + v1.y
	pz = v0.z + v1.z


	return V3(px,py,pz)


def sub(v0,v1):

	px = v0.x - v1.x
	py = v0.y - v1.y
	pz = v0.z - v1.z


	return V3(px,py,pz)

def mul(v0,k):
	px = v0.x * k
	py = v0.y * k
	pz = v0.z * k

	return V3(px,py,pz)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0,v1):
	p1 = v0.y * v1.z - v0.z * v1.y
	p2 = v0.z * v1.x - v0.x * v1.z
	p3 = v0.x * v1.y - v0.y * v1.x

	return V3(p1,p2,p3)

def length(v0):
	px = v0.x ** 2
	py = v0.y ** 2
	pz = v0.z ** 2
	len = (px+py+pz)**0.5
	return len

def norm(v0):
	v0Lon = length(v0)

	if not v0Lon:
		return V3(0,0,0)

	px = v0.x/v0Lon
	py = v0.y/v0Lon
	pz = v0.z/v0Lon

	return V3(px,py,pz)

def bbox(*vertices):
	xs = [vertex.x for vertex in vertices]
	ys = [vertex.y for vertex in vertices]
	xs.sort()
	ys.sort()
	'''
	p1 = xs[0], ys[0]
	p2 = xs[-1], ys[-1]
	'''
	return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

def baricentricas(A,B,C,P):
	bcoor = cross(
		V3(C.x - A.x, B.x - A.x, A.x - P.x),
		V3(C.y - A.y, B.y - A.y, A.y - P.y)
	)

	if abs(bcoor.z) < 1:
		return(-1,-1,-1)

	return (1 - (bcoor.x + bcoor.y) / bcoor.z, bcoor.y / bcoor.z, bcoor.x / bcoor.z)

def teorema(filas, columna):
	matriz = []
	for i in range(filas):
		#Añadimos una lista vacia
		matriz.append([])
		for j in range(columna):
			matriz[-1].append(0.0)
	return matriz

def multiplicarMatrices(m1,m2):

	"""
		MATRIZ 1			MATRIZ 2
	[ 0, 0 , 0 , 0 ]	[ 0, 0 , 0 , 0 ]
	[ 0, 0 , 0 , 0 ]	[ 0, 0 , 0 , 0 ]
	[ 0, 0 , 0 , 0 ]	[ 0, 0 , 0 , 0 ]
	[ 0, 0 , 0 , 0 ]	[ 0, 0 , 0 , 0 ]
	"""
	matrizResultante = teorema(len(m1), len(m2[0]))
	for i in range(len(m1)):
		for j in range(len(m2[0])):
			for k in range(len(m2)):
				matrizResultante[i][j] += m1[i][k] * m2[k][j]
	return matrizResultante


class Bitmap(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.framebuffer = []
		self.color = color(255,255,255)
		self.vertexColor = color(255,255,255)
		self.glCreateWindows()
		self.clear()
		self.zbuffer = [
			[-float('inf') for x in range(self.width)]
			for y in range(self.height)
		]

	def write(self,filename="out.bmp"):
		f = open(filename,'bw')
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(14 + 40))

		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		for x in range(self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])
		f.close()

	def archivo(self, filename='out.bmp'):
		self.write(filename)

	def glCreateWindows(self):
		self.framebuffer = [[0 for x in range(self.height)] for y in range(self.width)]

	def clear(self):
		self.framebuffer = [[color(0, 0, 0) for x  in range(self.width)] for y in range(self.height)]
		self.zbuffer = [[-float('inf') for x in range(self.width)] for y in range(self.height)]

	def glClearColor(self, r,g,b):
		R = int(r*255)
		G = int(g*255)
		B = int(b*255)
		self.framebuffer = [
			[color(R,G,B)
			for x in range(self.width)]
			for y in range(self.height)]

	def glViewPort(x,y,width,height):
		self.x = x
		self.y = y
		self.width_vp = width
		self.heigth_vp = heigth

	def glVertex(self, x, y):
		vertex_x = int((x+1)*(self.width_vp*0.5)) + self.x
		vertex_y = int((y+1)*(self.heigth_vp*0.5)) + self.y
		try:
			if (x==1) and (y==1):
				vertex_x = vertex_x - 1
				vertex_y = vertex_y - 1
		except IndexError:
			print('Revise los valores ingresados para el glViewPort')
		return (vertex_x,vertex_y)

	def glColor(self, r,g,b):
		self.vertexColor = color(r,g,b)

	def point(self, x, y,color=None):
		self.framebuffer[y][x]= color or self.vertexColor

	def glLine(self, vertex1, vertex2):
		x1 = vertex1[0]
		y1 = vertex1[1]
		x2 = vertex2[0]
		y2 = vertex2[1]

		dx = abs(x2-x1)
		dy = abs(y2-y1)
		st = dy > dx
		if dx == 0:
			for y in range(y1, y2+1):
				self.point(x1, y)
			return 0
		if(st):
			x1,y1 = y1,x1
			x2,y2 = y2,x2
		if(x1>x2):
			x1,x2 = x2,x1
			y1,y2 = y2,y1
		dx = abs(x2-x1)
		dy = abs(y2-y1)
		llenar = 0
		limite = dx
		y = y1
		for x in range(x1,(x2+1)):
			if (st):
				self.point(y,x)
			else:
				self.point(x,y)
			llenar += dy * 2
			if llenar >= limite:
				y += 1 if y1 < y2 else -1
				limite += 2*dx

	def triangulos(self, A, B, C, color=None,texture=None, tc=(), intensity=1):
		bbox_min, bbox_max = bbox(A,B,C)
		for x in range(bbox_min.x, bbox_max.x + 1):
			for y in range(bbox_min.y, bbox_max.y + 1):
				w, v, u = baricentricas(A, B, C, V2(x, y))
				if w < 0 or v < 0 or u < 0:
					continue
				if texture:
					tA, tB, tC = tc
					tx = tA.x * w + tB.x * v + tC.x * u
					ty = tA.y * w + tB.y * v + tC.y * u
					color = texture.get_color(tx, ty, intensity)
				z = A.z * w + B.z * v + C.z * u
				if x < self.width and y<self.height and x >=0 and y>=0:
					if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
						self.point(x, y, color)
						self.zbuffer[x][y] = z


	def transform(self, vector, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
		newMatriz = [[vector.x],[vector.y],[vector.z],[1]]
		mV = multiplicarMatrices(self.viewPortM, self.projection)
		view = multiplicarMatrices(mV, self.View_Matriz)
		vP = multiplicarMatrices(view, self.Model)
		newVertex = multiplicarMatrices(vP,newMatriz)
		a = round((newVertex[0][0])/newVertex[3][0])
		b = round((newVertex[1][0])/newVertex[3][0])
		c = round((newVertex[2][0])/newVertex[3][0])
		return (V3(a,b,c))

	def load(self, filename, mtlFile=None, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0), ojo=V3(0,0,0), arriba=V3(0,0,0), centro=V3(0,0,0), texture=None):
		objetos = Obj(filename, mtlFile)
		self.ModelMatriz(translate,scale,rotate)
		self.lookAt(ojo, arriba, centro)
		self.ViewPortMatriz()
		if mtlFile:
			mtl = Mtl(mtlFile)
			vR = mtl.materiales[0][0]
			vG = mtl.materiales[0][1]
			vB = mtl.materiales[0][2]
		ligth = V3(0,0,1)
		caras = objetos.faces
		vertexes = objetos.vertices

		for face in caras:
			vcount = len(face)
			if vcount == 3:
				f1 = face[0][0] - 1
				f2 = face[1][0] - 1
				f3 = face[2][0] - 1
				a = self.transform(V3(*vertexes[f1]),translate, scale)
				b = self.transform(V3(*vertexes[f2]),translate, scale)
				c = self.transform(V3(*vertexes[f3]),translate, scale)
				'''
				print('1', a)
				print('2', b)
				print('3', c)
				'''
				vector_normal = norm(cross(sub(b,a), sub(c,a)))
				intensidad = dot(vector_normal, ligth)
				if not texture:
					red = round(255*intensidad)
					green = round(255*intensidad)
					blue = round(255*intensidad)
					#Evitamos los numeros negativos
					if (red<0) or (green<0) or (blue<0):
						continue
					self.triangulos(a,b,c, color(red,green,blue))
				else:
					t1 = face[0][0] - 1
					t2 = face[1][0] - 1
					t3 = face[2][0] - 1
					Texture_A = self.transform(V3(*objetos.vt[t1],0))
					Texture_B = self.transform(V3(*objetos.vt[t2],0))
					Texture_C = self.transform(V3(*objetos.vt[t3],0))
					self.triangulos(Texture_A,Texture_B,Texture_C, color=None, texture=texture, tc=(Texture_A,Texture_B,Texture_C), intensity=intensidad)

	def ModelMatriz(self, translate, scale, rotate):
		translate = V3(*translate)
		scale = V3(*scale)
		rotate = V3(*rotate)
		matrixTranslate = [[0 for x in range(4)] for y in range(4)]
		matrixTranslate = [
			[1,0,0, translate.x],
			[0,1,0, translate.y],
			[0,0,1, translate.z],
			[0,0,0,1]
		]
		matrizScale = [
			[scale.x,0,0,0],
			[0,scale.y,0,0],
			[0,0,scale.z,0],
			[0,0,0,1]
		]
		matrizRotateX = [
			[1,0,0,0],
			[0,cos(rotate.x),-sin(rotate.x),0],
			[0,sin(rotate.x), cos(rotate.x),0],
			[0,0,0,1]
		]
		matrizRotateY = [
			[cos(rotate.y),0,sin(rotate.y),0],
			[0,1,0,0],
			[sin(rotate.y),0,cos(rotate.y),0],
			[0,0,0,1]
		]
		matrizRotateZ = [
            [cos(rotate.z),-sin(rotate.z),0,0],
            [sin(rotate.z), cos(rotate.z),0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]
		rotateMatriz = multiplicarMatrices(multiplicarMatrices(matrizRotateX,matrizRotateY) ,matrizRotateZ)
		self.Model = multiplicarMatrices(multiplicarMatrices(matrixTranslate,rotateMatriz), matrizScale)

	def ViewPortMatriz(self,x=0,y=0):
		self.viewPortM = [
			[(self.width*0.5),0,0,(x+self.width*0.5)],
			[0,(self.height*0.5),0,(y+self.height*0.5)],
			[0,0,128,128],
			[0,0,0,1]
		]

	def ProjectionMatriz(self, coeficiente):
		self.projection = [
			[1,0,      0	,0],
			[0,1,	   0	,0],
			[0,0,      1	,0],
			[0,0,coeficiente,1]
		]

	def ViewMatriz(self, x, y, z, center):
		#Matriz de x
		MX = [
			[(x.x),(x.y),(x.z), 0],
			[(y.x),(y.y),(y.z), 0],
			[(z.x),(z.y),(z.z), 0],
			[0,0,0,		1		 ]
		]
		MY = [
			[1,0,0,(-1*center.x)],
			[0,1,0,(-1*center.y)],
			[0,0,0,(-1*center.z)],
			[0,0,0,   	1		]
		]
		self.View_Matriz = multiplicarMatrices(MX,MY)

	def lookAt(self, ojo, arriba, centro):
		z = norm(sub(ojo,centro))
		x = norm(cross(arriba,z))
		y = norm(cross(z,x))
		self.ViewMatriz(x,y,z, centro)
		valor = norm(sub(ojo,centro))
		self.ProjectionMatriz(-1/length(sub(ojo,centro)))
