import glob, os
from os import walk
li = []
os.chdir("c:/slike/zito/")
for file in glob.glob("*.jpg"):
    li.append(os.path.splitext(file)[0])


for a in li:
    print a
    
for item in li:
    filePath = 'c:/slike/zito/%s.txt' % (item)
    open(filePath, 'w')
    
pomocno = "pomocni_tekst"
def klasa(file):
    print file+file

print klasa(pomocno)


for i in range(len(li)):
    print(li[i])



