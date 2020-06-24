
slika='c:\slike\Zito\DJI_0060.jpg'

import glob
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

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
    if i.upper() == 'W':
        deg = deg * -1
    elif i.upper() == 'S':
        deg = deg * -1
    return float(deg)
  
def gps(exif):
    lat = None
    lon = None
    if exif['GPSInfo']:        
        # Lat
        coords = exif['GPSInfo']
        i = coords[1]
        d = coords[2][0][0]
        m = coords[2][1][0]
        s = coords[2][2][0]
        lat = dms2dd(d, m ,s, i)
        # Lon
        i = coords[3]
        d = coords[4][0][0]
        m = coords[4][1][0]
        s = coords[4][2][0]
        lon = dms2dd(d, m ,s, i)
    return lat, lon

print gps(exif(slika))[0]







