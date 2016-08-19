#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, glob, os
from PIL import Image, ImageFilter

def mini(elemento, arquivo):
    # Retorna o nome do arquivo sem extensão
    f = glob.os.path.splitext(arquivo)[0]
    imagem = Image.open(elemento + arquivo)
    # Cria thumbnail (miniatura) da imagem
    # de tamanho 256x256 usando antialiasing
    imagem.thumbnail((128, 128), Image.ANTIALIAS)
    # Filtro suaviza a imagem
    imagem = imagem.filter(ImageFilter.SMOOTH)
    #Acesso o diretório mini
    os.chdir('mini')
    # Salva como arquivo PNG
    imagem.save('miniatura_'+ f + '.png', 'PNG')
    #Retorna na árvore de diretórios
    os.chdir("..")
