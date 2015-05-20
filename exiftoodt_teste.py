#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

## importa as bibliotecas que serao usadas no programa
import sys,os,platform,commands,subprocess
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import H, P, Span
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.draw  import Page, Frame, TextBox, Image
##from PIL import Image

def busca(diretorio):
    ## cria listas para armazenar conteudo, alem de iniciar variaveis,
    ## incluindo a que define as extensoes de imagem
    pastas = []
    sistema = platform.system()
    extensions = ['.jpeg', '.jpg', '.jpe', '.tga', '.gif', '.tif', '.bmp', '.rle', '.pcx', '.png', '.mac', '.pnt', '.pntg', '.pct', '.pic', '.pict', '.qti', '.qtif']

    ## procura todas as pastas dentro do diretorio especificado
    for caminho, files, docs in os.walk(diretorio):
        pastas.append(caminho)

    ## varre cada pasta em busca de arquivos
    for elemento in pastas:
        arquivos = os.listdir(elemento)
        for arquivo in arquivos:
            tipo = os.path.splitext(arquivo)
            if tipo[1] in extensions: ## se for arquivo de imagem
                ## roda comandos diferentes em linux e windows
                if sistema == "Linux":
                    extrailin(elemento, arquivo)
                elif sistema == "Windows":
                    extraiwin(elemento, arquivo)
                else:
                    print "Sistema nao suportado"
                    sys.exit(1)

def extraiwin(elemento, arquivo):
    cmd = 'python exif.py "' + elemento + '\\' + arquivo + '"'
    print 'Processando arquivo: ' + elemento + '\\' + arquivo
    texto = subprocess.check_output(cmd)
    escreve(texto)

def extrailin(elemento, arquivo):
    cmd = 'python exif.py "' + elemento + '/' + arquivo + '"'
    print 'Processando arquivo: ' + elemento + '/' + arquivo
    (status, texto) = commands.getstatusoutput(cmd)
    if status:
        sys.stderr.write(texto)
        sys.exit(1)
    escreve(texto)

def escreve(texto): 
    linhas = texto.split('\n')
    tr = TableRow()
    table.addElement(tr)
    celula = TableCell()
    tr.addElement(celula)
    tc = TableCell()
    tr.addElement(tc)
    p = []
    num = 0
    for linha in linhas:
        p.append(P(stylename=tablecontents,text=""))
        p[num].addText(linha)
        tc.addElement(p[num])
        num = num + 1

def main():    
    busca(sys.argv[1])

    doc.text.addElement(table)
    doc.save("testepython.odt")
    print "Metadados gravados com sucesso no arquivo testepython.odt"

if __name__ == '__main__':
    doc = OpenDocumentText()

    ## cria o estilo para o titulo do documento
    s = doc.styles
    h1style = Style(name="Heading 1", family="paragraph")
    h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold"}))
    s.addElement(h1style)
    h=H(outlinelevel=1, stylename=h1style, text="Arquivo de Metadados")
    doc.text.addElement(h)
    global tablecontents
    tablecontents = Style(name="Table Contents", family="paragraph")
    tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
    s.addElement(tablecontents)

    ## cria os padroes de coluna, com dois tamanhos, 5 e 15 cm
    widthshort = Style(name="Wshort", family="table-column")
    widthshort.addElement(TableColumnProperties(columnwidth="5cm"))
    doc.automaticstyles.addElement(widthshort)
    widthwide = Style(name="Wwide", family="table-column")
    widthwide.addElement(TableColumnProperties(columnwidth="15cm"))
    doc.automaticstyles.addElement(widthwide)

    ## cria a tabela e especifica as colunas
    global table
    table = Table()
    table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthshort))
    table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthwide))

    main()
