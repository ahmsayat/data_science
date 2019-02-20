import numpy, django, imageio, pandas
from scipy.misc import imread, imsave, imresize

print ("hello world")

a = numpy.array( [ [1,2,3] , [4,5,6] ] )
print (a.shape)

#print( a > 2 )

a = numpy.random.random( (2,2) )

#print (a)

img = imageio.imread('blond.png')
print (img.shape)

#img_tinted = img * [1, 0.95, 0.9]
#img_tinted = imresize(img, (300, 300))
#img_tinted = numpy.array( numpy.Image.fromarray(img).resize() )

# Write the tinted image back to disk
imageio.imsave('assets/cat_tinted.png', img_tinted)