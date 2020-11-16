import os
import sys
import pdb
import code
import xml.etree.ElementTree as ET
import math
import numpy as np
from PIL import Image

class Surface:
        def __init__(self):
                return
                
        def intersects(self):
                return
                
        def surface_norm(self):
                return
                
class Sphere(Surface):
	def __init__(self, origin, radius, oColor):
		self.origin = origin
		self.radius = radius
		self.oColor = oColor

	def intersects(self, ray):
		sphere_to_ray = ray.origin - self.origin
		b = 2 * ray.direction * sphere_to_ray
		c = sphere_to_ray ** 2 - self.radius ** 2
		discriminant = b ** 2 - 4 * c

		if discriminant >= 0:
			dist = (-b - math.sqrt(discriminant)) / 2
			if dist > 0:
				return dist

	def surface_norm(self, pt):
		return (pt - self.origin).normalize()


class Box(Surface):
    def __init__(self, downL, upR, oColor):
        self.oColor = oColor
        self.downL = downL
        self.upR = upR
    
    def surface_norm(self, m):
        if m.x < self.downL.x + .005 and m.x > self.downL.x - .005:
            return np.array([-1, 0, 0]).astype(float)
        elif m.x < self.upR.x + .005 and m.x > self.upR.x - .005:
            return np.array([1, 0, 0]).astype(float)
        elif m.y < self.downL.y + .005 and m.y > self.downL.y - .005:
            return np.array([0, -1, 0]).astype(float)
        elif m.y < self.upR.y + .005 and m.y > self.upR.y - .005:
            return np.array([0, 1, 0]).astype(float)
        elif m.z < self.downL.z + .005 and m.z > self.downL.z - .005:
            return np.array([0, 0, -1]).astype(float)
        else:
            return np.array([0, 0, 1]).astype(float)
    
    def intersects(self, Ray):
        if Ray.direction.x >= 0:  
            min_t = (self.downL.x - Ray.origin.x) / (Ray.direction.x + .01)
            max_t = (self.upR.x - Ray.origin.x) / (Ray.direction.x + .01)
        else:
            min_t = (self.upR.x - Ray.origin.x) / (Ray.direction.x + .01)
            max_t = (self.downL.x - Ray.origin.x) / (Ray.direction.x + .01)
        
        if Ray.direction.y >= 0:  
            min_ty = (self.downL.y - Ray.origin.y) / (Ray.direction.y + .01)
            max_ty = (self.upR.y - Ray.origin.y) / (Ray.direction.y + .01)
        else:
            min_ty = (self.upR.y - Ray.origin.y) / (Ray.direction.y + .01)
            max_ty = (self.downL.y - Ray.origin.y) / (Ray.direction.y + .01)

        if (min_t > max_ty) or (min_ty > max_t):
          return 

        if Ray.direction.z >= 0:  
            min_tz = (self.downL.z - Ray.origin.z) / (Ray.direction.z +0.1)
            max_tz = (self.upR.z - Ray.origin.z) / (Ray.direction.z +0.1)
        else:
            min_tz = (self.upR.z - Ray.origin.z) / (Ray.direction.z +0.1)
            max_tz = (self.downL.z - Ray.origin.z) / (Ray.direction.z +0.1)

        if (max(min_t, min_ty) > max_tz) or (min_tz > min(max_t, max_ty)):
            return

        if max(min_t, min_tz) >= 0:
            return 1/(max(min_t, min_tz))
        elif max(min_t, min_tz) < 0 and min(max_t, max_tz) >= 0:
            return 1/(min(max_t, max_tz))
        else: return
        
class Scene:
	def __init__(self, camera, objects, lights, width, height, viewUp, viewDir, projDistance, viewProjNormal,windowWidth,windowHeight):
		self.camera = camera
		self.objects = objects
		self.lights = lights
		self.width = width
		self.height = height
		self.viewUp = viewUp
		self.viewDir = viewDir
		self.projDistance = projDistance
		self.viewProjNormal = viewProjNormal
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		
	def render(self):
		viewP = np.array([self.camera.x,self.camera.y,self.camera.z])
		W = self.viewProjNormal
		W = W/np.sqrt((W**2).sum())
		U = np.cross(self.viewUp,W)
		U = U/np.sqrt((U**2).sum())
		V = np.cross(W,U)
		V = -V/np.sqrt((V**2).sum())
		S = viewP - W*self.projDistance
		L = S - U*(self.windowWidth/2) - V*(self.windowHeight/2)	
		pixels = [
			[Color() for _ in range(self.width)] for _ in range(self.height)]
		for i in range(self.height):
			for j in range(self.width):
				D = L + (U*j*(self.windowWidth/self.width))+(V*i*(self.windowHeight/self.height))
				D = D - viewPoint
				ray_direction = Point(D[0],D[1],D[2])
				ray = Ray(self.camera, ray_direction)
				pixels[i][j] = self._trace_ray(ray)
		
		return pixels

	def _trace_ray(self, ray, depth=0, max_depth=5):

		color = Color()

		if depth >= max_depth:
			return color

		intersection = self._get_intersection(ray)
		if intersection is None:
			return color

		obj, dist = intersection
		intersection_pt = ray.point_at_dist(dist)
		surface_norm = obj.surface_norm(intersection_pt)

		color += obj.oColor.color * obj.oColor.ambient

		for light in self.lights:
			break
			LightP_vec = (light - intersection_pt).normalize()
			LightP_ray = Ray(intersection_pt, LightP_vec)
			if self._get_intersection(LightP_ray) is None:
				lambert_intensity = surface_norm * LightP_vec
				if lambert_intensity > 0:
					color += obj.oColor.color * obj.oColor.lambert * \
						lambert_intensity

		return color

	def _get_intersection(self, ray):

		intersection = None
		for obj in self.objects:
			dist = obj.intersects(ray)
			if dist is not None and \
				(intersection is None or dist < intersection[1]):
				intersection = obj, dist

		return intersection

class Vector:


	def __init__(self, x=0., y=0., z=0.):
		self.x = x
		self.y = y
		self.z = z

	def norm(self):
		return math.sqrt(sum(num * num for num in self))

	def normalize(self):
		return self / self.norm()

	def reflect(self, other):
		other = other.normalize()
		return self - 2 * (self * other) * other

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other):
		if isinstance(other, Vector):
			return self.x * other.x + self.y * other.y + self.z * other.z;
		else:
			return Vector(self.x * other, self.y * other, self.z * other)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __truediv__(self, other):
		return Vector(self.x / other, self.y / other, self.z / other)

	def __pow__(self, exp):
		return self * self

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z

Point = Vector
Color = Vector





		
class OColor:
	def __init__(self, color, specular=1., lambert=1., ambient=1.):
		self.color = color
		self.specular = specular
		self.lambert = lambert
		self.ambient = ambient


class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction.normalize()

	def point_at_dist(self, dist):
		return self.origin + self.direction * dist


if __name__ == "__main__":
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	projDistance=1.0
	position=np.array([0,0,0]).astype(np.float)
	intensity=np.array([1,1,1]).astype(np.float)
	imgSize=np.array(root.findtext('image').split()).astype(np.int)
	channels=3
	img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
	img[:,:]=0

	for c in root.findall('camera'):
		viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float)
		viewDir=np.array(c.findtext('viewDir').split()).astype(np.float)
		viewProjNormal=np.array(c.findtext('projNormal').split()).astype(np.float)
		viewUp=np.array(c.findtext('viewUp').split()).astype(np.float)
		if(c.findtext('projDistance')):
                        projDistance = float(c.findtext('projDistance'))
		viewWidth=float(c.findtext('viewWidth'))
		viewHeight=float(c.findtext('viewHeight'))

	sphere_center = []
	sphere_radius = []
	sphere_color = []
	box_max =[]
	box_min =[]
	box_color = []

	for c in root.findall('shader'):
                if(c.get('name') == 'red'):
                        color_red = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'green'):
                        color_green = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'blue'):
                        color_blue = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'gray'):
                        color_gray = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball000'):
                        color_ball000 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball001'):
                        color_ball001 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball010'):
                        color_ball010 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball011'):
                        color_ball011 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball100'):
                        color_ball100 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball101'):
                        color_ball101 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball110'):
                        color_ball110 = np.array(c.findtext('diffuseColor').split()).astype(np.float)
                elif(c.get('name') == 'ball111'):
                        color_ball111 = np.array(c.findtext('diffuseColor').split()).astype(np.float)                       
                elif(c.get('name') == 'stick'):
                        color_stick = np.array(c.findtext('diffuseColor').split()).astype(np.float)                             
	for c in root.findall('surface'):
                if(c.get('type') == 'Sphere'):
                        
                        for q in c.findall('shader'):
                                my_ref = q.get('ref')
                        sphere_color.append(my_ref)
                        center_c = np.array(c.findtext('center').split()).astype(np.float)
                        sphere_center.append(center_c)
                        radius_c = float(c.findtext('radius'))
                        sphere_radius.append(radius_c)
                elif(c.get('type') == 'Box'):
                        for q in c.findall('shader'):
                                my_ref = q.get('ref')
                        box_color.append(my_ref)
                        max_c = np.array(c.findtext('maxPt').split()).astype(np.float)
                        box_max.append(max_c)
                        min_c = np.array(c.findtext('minPt').split()).astype(np.float)
                        box_min.append(min_c)
	objects=[]
	lights = []

	for c in root.findall('light'):
		position=np.array(c.findtext('position').split()).astype(np.float)
		lights.append(Point(position[0],position[1],position[2]))
		intensity=np.array(c.findtext('intensity').split()).astype(np.float)
	objects = []
        
	for r in range(len(sphere_radius)):
                if(sphere_color[r]=='red'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_red[0]*255, color_red[1]*255, color_red[2]*255),specular=0.)))
                elif(sphere_color[r]=='blue'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_blue[0]*255, color_blue[1]*255, color_blue[2]*255),specular=0.)))
                elif(sphere_color[r]=='gray'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_gray[0]*255, color_gray[1]*255, color_gray[2]*255),specular=0.)))
                elif(sphere_color[r]=='green'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_green[0]*255, color_green[1]*255, color_green[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball000'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball000[0]*255, color_ball000[1]*255, color_ball000[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball001'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball001[0]*255, color_ball001[1]*255, color_ball001[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball010'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball010[0]*255, color_ball010[1]*255, color_ball010[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball011'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball011[0]*255, color_ball011[1]*255, color_ball011[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball100'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball100[0]*255, color_ball100[1]*255, color_ball100[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball101'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball101[0]*255, color_ball101[1]*255, color_ball101[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball110'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball110[0]*255, color_ball110[1]*255, color_ball110[2]*255),specular=0.)))
                elif(sphere_color[r]=='ball111'):
                        objects.append(Sphere(Point(sphere_center[r][0],sphere_center[r][1],sphere_center[r][2]), sphere_radius[r], OColor(Color(color_ball111[0]*255, color_ball111[1]*255, color_ball111[2]*255),specular=0.)))

	for r in range(len(box_min)):
                if(box_color[r]=='red'):
                        objects.append(Box(Point(box_min[r][0],box_min[r][1],box_min[r][2]),Point(box_max[r][0],box_max[r][1],box_max[r][2]),OColor(Color(color_red[0]*255, color_red[1]*255, color_red[2]*255),specular=0.)))
                elif(box_color[r]=='blue'):
                        objects.append(Box(Point(box_min[r][0],box_min[r][1],box_min[r][2]),Point(box_max[r][0],box_max[r][1],box_max[r][2]), OColor(Color(color_blue[0]*255, color_blue[1]*255, color_blue[2]*255),specular=0.)))
                elif(box_color[r]=='gray'):
                        objects.append(Box(Point(box_min[r][0],box_min[r][1],box_min[r][2]),Point(box_max[r][0],box_max[r][1],box_max[r][2]), OColor(Color(color_gray[0]*255, color_gray[1]*255, color_gray[2]*255),specular=0.)))
                elif(box_color[r]=='green'):
                        objects.append(Box(Point(box_min[r][0],box_min[r][1],box_min[r][2]),Point(box_max[r][0],box_max[r][1],box_max[r][2]), OColor(Color(color_green[0]*255, color_green[1]*255, color_green[2]*255),specular=0.)))
                elif(box_color[r]=='stick'):
                        objects.append(Box(Point(box_min[r][0],box_min[r][1],box_min[r][2]),Point(box_max[r][0],box_max[r][1],box_max[r][2]), OColor(Color(color_stick[0]*255, color_stick[1]*255, color_stick[2]*255),specular=0.)))

	camera = Point(viewPoint[0], viewPoint[1], viewPoint[2])
	scene = Scene(camera, objects, lights, imgSize[0], imgSize[1],viewUp,viewDir,projDistance,viewProjNormal,viewWidth,viewHeight)
	pixels = scene.render()
	for i in range(imgSize[1]):
		for j in range(imgSize[0]):
			img[i][j] = np.array([pixels[i][j].x,pixels[i][j].y,pixels[i][j].z])
	rawimg = Image.fromarray(img,'RGB')
	rawimg.save(sys.argv[1]+'.png')
