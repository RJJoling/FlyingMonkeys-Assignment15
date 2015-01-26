## Team:                                                Team Members:                                        Date:
## FlyingMonkeys                                  Damiano Luzzi                                         23-01-2015
##                                                          Robbert-Jan Joling

## Import modules
import os  # for finding the working directory
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np

## Register GDAL drivers
print "the GDAL version"
print(gdal.__version__)
gdal.AllRegister()

## Check working directory
print "Working directory:",  os.getcwd()

## Opening Erdas Imagine Images (*.tif)
driver = gdal.GetDriverByName('GTiff')

filename = 'Raster/data/LC81980242014260LGN00_sr_band4.tif'
filename2 = 'Raster/data/LC81980242014260LGN00_sr_band5.tif'

dataSource = gdal.Open(filename, GA_ReadOnly)
dataSource2 = gdal.Open(filename2,  GA_ReadOnly)

## Transform bands into arrays
band4 = dataSource.GetRasterBand(1)
band4Arr = band4.ReadAsArray(0,0,dataSource.RasterXSize, dataSource.RasterYSize)

band5 = dataSource2.GetRasterBand(1)
band5Arr = band5.ReadAsArray(0,0,dataSource2.RasterXSize, dataSource2.RasterYSize)

## Change data type
band4Arr=band4Arr.astype(np.float32)
band5Arr=band5Arr.astype(np.float32)

## Create mask to select non-zero value
mask = np.greater(band4Arr+band5Arr,  0) 
ndwi = np.choose(mask,(-99, (band4Arr-band5Arr)/(band4Arr+band5Arr))) 
# For some reason still returns a divide by zero warning!
print "NDWI min and max values", ndwi[ndwi>-99].min(), ndwi.max()

## Output an image
outDataSet=driver.Create('Raster/data/ndwi.tif', dataSource.RasterXSize, dataSource.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(ndwi,0,0)
outBand.SetNoDataValue(-99)

## Set projection to input source projection
outDataSet.SetProjection(dataSource.GetProjection())

## Save and clean memory
outBand.FlushCache()
outDataSet.FlushCache()
