#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os,sys,getopt,struct
from cStringIO import StringIO
from odf.opendocument import OpenDocumentPresentation
from odf.style import Style, MasterPage, PageLayout, PageLayoutProperties, \
TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties
from odf.text import P
from odf.draw  import Page, Frame, TextBox, Image

def getImageInfo(data):
    size = len(data)
    height = -1
    width = -1
    w = -1
    h = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG v1.2 spec (http://www.cdrom.com/pub/png/spec/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and (data[:8] == '\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and (data[:8] == '\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and (data[:2] == '\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except: pass

    return content_type, width, height


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    n = 1
    m = 1
    for elemento in opts:
        print "opt " + str(n) + ":" + elemento
        n = n+1
    for elemento2 in args:
        print "arg " + str(m) + ":" + elemento2
    print len(args)
    diretorio = args[0]
    for imagem in os.listdir(diretorio):
        try:
            dadosimagem = open(diretorio + "\\" + imagem).read()
        except:
            continue
        ct,w,h = getImageInfo(dadosimagem)
        print imagem
        print ct
        print w
        print h