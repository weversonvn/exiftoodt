#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__="caio"
__date__ ="$14/11/2014 15:36:25$"
"""Cria miniaturas suavizadas para cada .jpg na pasta corrente"""
#O módulo de OS em Python fornece uma maneira de usar o sistema operacional em suas funcionalidades.
import os
# O módulo glob encontra todos os caminhos correspondentes a um padrão.
import glob
# Módulo principal do PIL.
import Image
# Módulo de filtros.
import ImageFilter

def mini():
    #Criamos um diretório chamado mini para guardar nossas imagens geradas
    os.mkdir ('Mini')
    #Definimos as extenções de imagens que o programa deve tratar.
    types = ('*.jpeg', '*.jpg', '.*jpe', '*.tga', '*.gif', '*.tif', '*.bmp','*.rle', '*.pcx', '*.mac', '*.png' , '*.pnt', '*.pntg', '*.pct', '*.pic','*.pict', '*.qti', '*.qtif')
    #o primeiro for vai trabalhar um a um os tipos na lista types.
    for files in types:
        #o segundo for vai fazer a varredurra na pasta corrente e encontrar as imagens.
        for fn in glob.glob(files):
            # Retorna o nome do arquivo sem extensão
            f = glob.os.path.splitext(fn)[0]
            print 'Processando:', fn
            imagem = Image.open(fn)
            # Cria thumbnail (miniatura) da imagem
            # de tamanho 256x256 usando antialiasing
            imagem.thumbnail((128, 128), Image.ANTIALIAS)
            # Filtro suaviza a imagem
            imagem = imagem.filter(ImageFilter.SMOOTH)
            #Acesso o diretório mini
            os.chdir('Mini')
            # Salva como arquivo PNG
            imagem.save('miniatura_'+ f + '.png', 'PNG')
            #Retorna na árvore de diretórios
            os.chdir("..")
            print 'Miniatura de ' + fn + ' criada com sucesso.'
            
#Rotina principal
#Chamada da função mini()
mini()
