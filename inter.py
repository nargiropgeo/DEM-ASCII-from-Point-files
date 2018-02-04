import sys
import numpy as np
from scipy.interpolate import griddata
import matplotlib.mlab as ml


""" Get args """
# Input txt point file in PENZ format
file_in = sys.argv[1]

# Grid resolution / Pixel size
pixel = np.float(sys.argv[2])

# Preferred interpolation method. linear or nearest neighbour(nn)
if not sys.argv[3]: method = 'linear'
else: method = 'nn'

# Output file
if sys.argv[4]: file_out = sys.argv[4]
else: file_out = sys.argv[1].replace('.txt', '_interp.asc')

# Change the number notation to floating point instead of scientific
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

# Vectors for coordinates and elevation values
x,y,z = np.loadtxt(sys.argv[1],delimiter=',',usecols=(1,2,3),unpack=True)

# Calculate output file dimensions
xmin = min(x)
ymin = min(y)
xmax = max(x)
ymax = max(y)
nrows = (ymax - ymin)/pixel
ncols = (xmax - xmin)/pixel

# Grid generation and interpolation
xi = np.linspace(min(x), max(x), num=ncols)
yi = np.linspace(min(y), max(y), num=nrows)
zi = ml.griddata(x, y, z, xi, yi, interp=method)
zi = np.fliplr(zi)
zi = np.rot90(zi, 2)

# Replace NaN values with -9999 suitable for ArcGIS
zi[np.isnan(zi)]=-9999

# ASCII file header
header = "ncols %d \nnrows %d\nxllcorner %f\nyllcorner %f\ncellsize %f\nnodata_value -9999" % (int(ncols), int(nrows), float(min(x)), float(min(y)), pixel)

# Save ASCII file
np.savetxt(dir_txt, zi, fmt='%f', header=header, comments='', delimiter=' ', newline='\n')
