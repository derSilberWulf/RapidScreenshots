import os, sys

#delete all the .png files in the currend directory

for file in os.listdir('.'):
    if(file.endswith('.png')):
        os.remove(file)
