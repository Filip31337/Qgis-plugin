from pyproj import Proj

Lat = 45.293628
Lon = 18.343028

ZoneNo = "34T" #Manually input, or calcuated from Lat Lon
myProj = Proj("+proj=utm +zone="+ZoneNo+",\
+north +ellps=WGS84 +datum=WGS84 +units=m +no_defs") #north for north hemisphere
UTMx, UTMy = myProj(Lon, Lat)
print UTMx, UTMy
print "za sada radi"