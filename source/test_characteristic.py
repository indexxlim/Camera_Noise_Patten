#!/usr/bin/env python

from make_characteristic import get_noise_from_file

import cPickle
import glob
import numpy
import sys

from PIL import Image, ImageOps

TILE_OVERLAP = 8

if len(sys.argv) != 3:
  print "Usage:\n\t%s noise_file_name path_with_png_files" % (sys.argv[0],)
  sys.exit(0)

noise_file_name = sys.argv[1]
image_path_name = sys.argv[2]
print image_path_name

# Load the camera noise.
camera_noise = numpy.loadtxt(noise_file_name, dtype=numpy.float)
camera_noise_average = numpy.average(numpy.nan_to_num(camera_noise))
camera_noise -= camera_noise_average
camera_noise_norm = numpy.sqrt(numpy.sum(numpy.nan_to_num(camera_noise * camera_noise)))

#print 'camera_noise_average : ', numpy.sum(camera_noise * camera_noise)[0]

#file_list = glob.glob(image_path_name + '/*.bmp')

types = ('*.pdf', '*.cpp', '/*.bmp', '/*.jpg', '/*png', '/*.bmp')
file_list = []
for files in types:
  file_list.extend(glob.glob(image_path_name + files))


print "Processing %d images" % (len(file_list),)
sumf = 0
for f in file_list:
  # Get this image's noise.
  image_noise =     (f)[1]
  image_noise_average = numpy.average(image_noise)
  image_noise -= image_noise_average
  image_noise_norm = numpy.sqrt(numpy.sum(image_noise * image_noise))

  # Calculate the correlation between the two signals.
  print "Dot product %s is: %s" % (f,
                                   numpy.sum(numpy.nan_to_num(camera_noise * image_noise)) /
                                     (camera_noise_norm * image_noise_norm))
  cor_v = numpy.sum(numpy.nan_to_num(camera_noise * image_noise)) / (camera_noise_norm * image_noise_norm)
  sumf = sumf + cor_v
print 'sumf : ', sumf
sumf = sumf / len(file_list)
print 'sumf(average) : ', sumf ,len(file_list)
