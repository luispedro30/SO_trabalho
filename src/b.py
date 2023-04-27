import os,re
for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
    path = path.split('..\\instances\\')[1].replace('\\','/')
    print(type(path))
