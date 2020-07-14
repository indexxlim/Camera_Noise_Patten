 #!/usr/bin/env python

import cPickle
import glob
import math
import numpy
import sys

# http://www.pybytes.com/pywavelets/ref/
import pywt

# http://www.pythonware.com/library/pil/handbook/index.htm
from PIL import Image, ImageOps

# Accelerator module for filtering.
from accel.filter_accel import wiener_filter

TILE_OVERLAP = 8 ##edge
TILE_SIZE = 256
DENOISE_SIGMA = 5
IMAGE_SIZE = 256

def denoise_coefficient_list(coefficient_list, sigma):
  ll = coefficient_list[0]
  denoised_bands = [ll]
  for band, subband_coefficients in enumerate(coefficient_list[1 :]):
    denoised_bands.append([wiener_filter(s.astype(numpy.float), sigma)
                           for s in subband_coefficients])
  return denoised_bands

def get_noise(greyscale_matrix):
  original_shape = greyscale_matrix.shape

  # The image will be transformed in TILE_SIZE * TILE_SIZE tiles with overlap
  # TILE_OVERLAP on each side.
  tiles_count = [(d - TILE_OVERLAP) / (TILE_SIZE - TILE_OVERLAP)
                 for d in original_shape]
  tiled_shape = [TILE_OVERLAP + c * (TILE_SIZE - TILE_OVERLAP)
                 for c in tiles_count]
  without_edges_shape = [c * (TILE_SIZE - TILE_OVERLAP) - TILE_OVERLAP
                         for c in tiles_count]
                         

  # The greyscale image is represented as a matrix of float values.
  greyscale_matrix = greyscale_matrix.astype(float)
  result_matrix = numpy.zeros(tiled_shape, dtype = numpy.float)

  # Work out how many levels of wavelet decomposition we will do.
  dyad_length = math.ceil(math.log(TILE_SIZE, 2))
  ll_levels = 5
  wavelet_levels = dyad_length - ll_levels
  ll_size = 2 ** ll_levels

  # Make a window for the tile edges.
  tile_window = numpy.zeros((TILE_SIZE, TILE_SIZE), dtype=numpy.float)
  tile_window[TILE_OVERLAP / 2 :
                -(TILE_OVERLAP / 2),
              TILE_OVERLAP / 2 :
                -(TILE_OVERLAP / 2)] = 1.0

  # Transform and filter each non-overlapping TILE_SIZE * TILE_SIZE square of
  # the image separately.
  for ty in range(0, tiles_count[1]):
    for tx in range(0, tiles_count[0]):
      transform_input = greyscale_matrix[
                          tx * (TILE_SIZE - TILE_OVERLAP) :
                            tx * (TILE_SIZE - TILE_OVERLAP) + TILE_SIZE,
                          ty * (TILE_SIZE - TILE_OVERLAP) :
                            ty * (TILE_SIZE - TILE_OVERLAP) + TILE_SIZE]
      coefficient_list = pywt.wavedec2(transform_input,
                                       'db8',
                                       level = int(wavelet_levels),
                                       mode = 'per')
          
      coefficient_list = denoise_coefficient_list(coefficient_list,
                                                  DENOISE_SIGMA)
      denoised_tile = pywt.waverec2(coefficient_list,
                                    'db8',
                                    mode = 'per')
      denoised_tile[denoised_tile > 255.0] = 255.0
      denoised_tile[denoised_tile < 0.0] = 0.0
      result_matrix[tx * (TILE_SIZE - TILE_OVERLAP) :
                      tx * (TILE_SIZE - TILE_OVERLAP) + TILE_SIZE,
                    ty * (TILE_SIZE - TILE_OVERLAP) :
                      ty * (TILE_SIZE - TILE_OVERLAP) + TILE_SIZE] += \
                      (denoised_tile * tile_window)

  # Remove the edges.
  result_matrix = result_matrix[TILE_OVERLAP : -TILE_OVERLAP,
                                TILE_OVERLAP : -TILE_OVERLAP]

  # Subtract the denoised image from the original to get an estimate of the
  # noise.
  original = greyscale_matrix[TILE_OVERLAP : tiled_shape[0] - TILE_OVERLAP,
                              TILE_OVERLAP : tiled_shape[1] - TILE_OVERLAP]
  print ('transform_input : ' ,transform_input.shape)
  print (original.shape)

  return (result_matrix, original - result_matrix)

def get_noise_from_file(file_name):
  original = Image.open(file_name)
  greyscale = ImageOps.grayscale(original)
  
  greyscale_vector = numpy.fromstring(greyscale.tobytes(), dtype=numpy.uint8)
  greyscale_matrix = numpy.reshape(greyscale_vector, (original.size[1], original.size[0]))

  greyscale_matrix = crop_center(greyscale_matrix,IMAGE_SIZE,IMAGE_SIZE) ##crop image
  
  return get_noise(greyscale_matrix)

def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)
    return img[starty:starty+cropy,startx:startx+cropx]


# Command line utility for creating the characteristic.
if __name__ == '__main__':
  if len(sys.argv) != 3:
    print ("Usage:\n\t%s path_with_png_files output_file_name" % (sys.argv[0],))
    sys.exit(0)

  # Get a list of images to process.
  types = ('*.pdf', '*.cpp', '/*.bmp', '/*.jpg', '/*png', '/*.bmp')
# file_list = glob.glob(sys.argv[1] + '/*.jpg')

  file_list = []
  for files in types:
      file_list.extend(glob.glob(sys.argv[1] + files))


  print ("Processing %d images" % (len(file_list),))

  # Denoise and build the numerator/denominator.
  numerator = None
  denominator = None
  for i, f in enumerate(file_list):
    print ("Processing %03d %s" % (i, f,))
    (denoised_matrix, residual_matrix) = get_noise_from_file(f)
    if numerator is None:
      numerator = numpy.zeros_like(residual_matrix)
      denominator = numpy.zeros_like(residual_matrix)
    numerator += denoised_matrix * residual_matrix        #residual_matrix = original - denoised_matrix
    denominator += denoised_matrix * denoised_matrix

#print (numerator / denominator).shape
  numpy.savetxt(sys.argv[2], numerator / denominator)
