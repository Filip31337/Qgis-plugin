import os

from osgeo import gdal,ogr,osr

print os.getcwd()

raster=r'c:\Slike\Zito\DJI_0060.jpg'

ds=gdal.Open(raster)

gt=ds.GetGeoTransform()
cols = ds.RasterXSize
rows = ds.RasterYSize
print cols, rows
ulx, xres, xskew, uly, yskew, yres  = ds.GetGeoTransform()
print uly, ulx


lon = 45.293682
lat = 18.343028

lgx = ((rows/360.0) * (180 + lon))
lgy = ((cols/180.0) * (90 - lat))

print "koordinate slike: ", lgx, lgy
