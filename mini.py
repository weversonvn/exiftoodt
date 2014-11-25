#!/usr/bin/env python
import os
from PIL import Image
 
cwd = os.getcwd()
for arquivo in os.listdir(cwd):
   print arquivo
   if arquivo.endswith('.jpg'):
      im = Image.open(arquivo)
      im.thumbnail((500,375), Image.ANTIALIAS)
      nome = arquivo.split('.')[0]
      mnome = nome + "_thumb.jpg"
      im.save(mnome, "JPEG")
      print '<a href="%s"><img src="%s"/></a><br/>' % (arquivo, mnome)
