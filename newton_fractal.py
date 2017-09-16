from numpy import sin,cos, log, exp, sqrt

def f(x):
    #return x**4 - 20
    return x**8-x**3+2 + sqrt(x)
def df(x):
    #return 4* x**3
    return 8*x**7-3*x**2 - .5/sqrt(x)

def newtons(z, f, df, max_n=100, epsilon=1e-10):
    z0 = z
    z1 = z0 - f(z0)/df(z0)
    for n in range(max_n):
        #print(z0, z1)
        if abs(z0-z1) < epsilon:
            return (n, z0)
        z0, z1 = z0 - f(z0)/df(z0), z0
    return (n, z0)
    
def secant(z, delta, f, max_n=100, epsilon=1e-10):
    z0 = z
    z1 = z0 + delta
    f0, f1 = f(z0), f(z1)
    for n in range(max_n):
        #print(z0, z1)
        if abs(z0-z1) < epsilon:
            return (n, z0)
        z0, z1 = z0 - (z1-z0)/(f1-f0)*f0, z0
        f0, f1 = f(z0), f0
    return (n, z1)


from PIL import Image
import sys
from math import pi

#**********************************************************

#My variables
aspect_ratio = 0.5625

res_quality = .25
x_center  = 0
y_center = 0
x_window_width = 3
y_window_width = x_window_width * aspect_ratio


#referenced variables
x_min = x_center - x_window_width / 2
x_max = x_center + x_window_width / 2
y_min = y_center + y_window_width / 2
y_max = y_center - y_window_width / 2

x_pixels = int(1920*res_quality)
y_pixels = int(1080*res_quality) #int(x_pixels * (y_max - y_min)/(x_max - x_min))

converge_cutoff = 2**1
iteration_count = 50
iteration_color_start = 0

#colors = [(10,10,10),(255,0,0),(255,200,200)] #reds
colors = [(10,0,0), (255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0, 255), (255,0,255), (255,200,255)] #rainbow

mandelbrot_color = (0,0,0) #black

def domain(z):
	return z #1/(z-1) #1/z + -3/4  #.2542585

#**********************************************************



#this is the range that the colors need to fill
iter_range = iteration_count - iteration_color_start
#this is the number of colors per gradient
gradient_span = iter_range//(len(colors)-1)

#The mapping from iteration count to a color.
color_map = []

for gradient in range(0,len(colors)-1):
	for gradient_unit in range(0,gradient_span):
		#each component is a weighted average of the gradients.
		r = (colors[gradient][0] * (gradient_span - gradient_unit) + colors[gradient+1][0] * gradient_unit)//gradient_span
		g = (colors[gradient][1] * (gradient_span - gradient_unit) + colors[gradient+1][1] * gradient_unit)//gradient_span
		b = (colors[gradient][2] * (gradient_span - gradient_unit) + colors[gradient+1][2] * gradient_unit)//gradient_span
		color_map.append((r,g,b))
color_map.append(colors[-1]) #Last would be first in next gradient iteration, so it must be added now.
color_map.append(mandelbrot_color) #These are determined to be in the set.
#due to rounding there may be fewer colors than iterations. The simplest solution is to redefine the iteration count
iteration_count = len(color_map) - 1
	
def x_to_re(x):
	#turns x pixel into real coordinate
	global x_pixels, x_min, x_max
	return x_min + x * (x_max - x_min) / (x_pixels-1)
	
def y_to_im(y):
	#turns y pixel into imaginary coordinate
	global y_pixels, y_min, y_max
	return y_min + y * (y_max - y_min) / (y_pixels-1)

def converge(z1):
	try:
		z = domain(z1)
	except:
		print('zero division at ' + str(z1))
		return 0
	cnt = 0
	return secant(z, z+.5/x_pixels, f, iteration_count)[0]
	#return newtons(z, f, df, iteration_count)[0]
	'''
	w = z
	while abs(w) < converge_cutoff and cnt!=iteration_count:
		w = w*w + z
		cnt += 1
	return cnt
	'''

img = Image.new('RGB', (x_pixels,y_pixels)) #new black image
pixels = img.load() # create the pixel map

print('\nCalculating...')
for x in range(img.size[0]):
	print( "{:.0f}".format(100*x//x_pixels) + '%', end='\r')
	for y in range(img.size[1]): # for every pixel:
		z = complex(x_to_re(x), y_to_im(y))
		n = converge(z)
		pixels[x,y] = color_map[n] # set the colour accordingly
print('100%')


img.show()

if len(sys.argv) > 1:
	file = sys.argv[1]
else:
	file = input('To save the image, enter a file name. Otherwise leave blank and press enter.\n')
	
if file != '' :
	img.save('pics//' +file + '.jpg', 'JPEG')
	print('Saved as ' + 'pics//' +file + '.jpg\n')
else:
	print('Did not save the output.\n')
