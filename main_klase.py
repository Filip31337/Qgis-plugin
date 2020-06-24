import glob
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pyproj import Proj
from osgeo import gdal, osr
from PyQt4.QtCore import QFile, QFileInfo
import os
from os import walk
#slika="c:\slike\Zito\DJI_0060.jpg"
#georef_slika="c:\Slike\Zito\Georeferencirana.tif"
radni_dir = 'c:/slike/Zito/testiranje/'
#-----------------Izvlaci LAT LONG----------------------------------------------------------------------------
def exif(img):
    exif_data = {}
    try:    
        i = Image.open(img)
        tags = i._getexif()
        for tag, value in tags.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    except:
        pass
    return exif_data
    
def dms2dd(d, m, s, i):
    sec = float((m * 60) + s)
    dec = float(sec / 3600)
    deg = float(d + dec)
    if i.upper() == "W":
        deg = deg * -1
    elif i.upper() == "S":
        deg = deg * -1
    return float(deg)
 
def gps(exif):
    lat = None
    lon = None
    if exif["GPSInfo"]:        
        # Lat
        coords = exif["GPSInfo"]
        i = coords[1]
        d = coords[2][0][0]
        m = coords[2][1][0]
        s = coords[2][2][0]
        lat = dms2dd(d, m ,s, i)
        lat = float(str(d)+str(m)+str(s))/100000000
        # Lon
        i = coords[3]
        d = coords[4][0][0]
        m = coords[4][1][0]
        s = coords[4][2][0]
        lon = float(str(d)+str(m)+str(s))/100000000
    return lat, lon

#------------------Pretvara LAT LONG u UTM----------------------------------------------------------------------------
def pretvarac(fotka):
    Lat = gps(exif(fotka))[0]
    Lon = gps(exif(fotka))[1]
    print "Lon/Lat Koordinate slike: ", Lon, " ",Lat
    ZoneNo = "34T" # rucno uneseno, a moze se izracunati unaprijed preko alt long
    myProj = Proj("+proj=utm +zone="+ZoneNo+",+north +ellps=WGS84 +datum=WGS84 +units=m +no_defs") # north za sjevernu hemisferu
    UTMx, UTMy = myProj(Lon, Lat)
    round(UTMx, 2)
    round(UTMy, 2)
    print "UTM Koordinate slike: ", UTMx, " ",UTMy
    global UTMx
    global UTMy
    return  UTMx, UTMy

#--------------------Georeferenciranje----------------------------------------------------------------------------
def georeferenciranje(src_filename,dst_filename):
    src_ds = gdal.Open(src_filename)
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    dst_ds = driver.CreateCopy(dst_filename, src_ds, 0)

    # Specify raster location through geotransform array
    # (uperleftx, scalex, skewx, uperlefty, skewy, scaley)
    # Scale = size of one pixel in units of raster projection
    # this example below assumes 100x100
    gt = [UTMx, 100, 0, UTMy, 0, -100]

    dst_ds.SetGeoTransform(gt)
    epsg = 3857
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    dest_wkt = srs.ExportToWkt()
    dst_ds.SetProjection(dest_wkt)
    dst_ds = None
    src_ds = None
#-----------------Ubacivanje u QGIS----------------------------------------------------------------------------
def ubacivanje(fileName):
    print "ubacujem raster"
    #fileName = dst_filename
    fileInfo = QFileInfo(fileName)
    baseName = fileInfo.baseName()
    rlayer = QgsRasterLayer(fileName, baseName)
    iface.addRasterLayer(fileName, "Raster Layer Zito")
    print "raster ubacen"

#----------------Folder loop------------------------------------------------------------------------------------
li = []
l = 0
os.chdir(radni_dir)
#Uzima listu sa imenima slika ( li )
for file in glob.glob("*.jpg"):
    li.append(os.path.splitext(file)[0])
    l+= 1
    pretvarac(file)
    gr = os.path.dirname(file)+str(l)+ '_georeferencirana'+'.tif'
    georeferenciranje(file,gr)
    ubacivanje(gr)
    



#pretvarac(slika)
#georeferenciranje(slika,georef_slika)
#ubacivanje(georef_slika)



