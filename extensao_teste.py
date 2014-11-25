##!/usr/bin/python -tt

## Importa as bibliotecas que serao usadas no programa
import sys,os,platform,commands,subprocess
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import H, P, Span
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.draw  import Page, Frame, TextBox, Image
##from PIL import Image

def extrai(diretorio):
    pastas = []
    metadados = []
    cont = 0
    sistema = platform.system()
    extensions = ['.jpeg', '.jpg', '.jpe', '.tga', '.gif', '.tif', '.bmp', '.rle', '.pcx', '.png', '.mac', '.pnt', '.pntg', '.pct', '.pic', '.pict', '.qti', '.qtif']
    for caminho, files, docs in os.walk(diretorio):
        pastas.append(caminho)
    for elemento in pastas:
        arquivos = os.listdir(elemento)
        for arquivo in arquivos:
            tipo = os.path.splitext(arquivo)
            if tipo[1] in extensions:
                if sistema == "Linux":
                    cmd = 'python exif.py "' + elemento + '/' + arquivo + '"'
                    (status, texto) = commands.getstatusoutput(cmd)
                    if status:
                        sys.stderr.write(texto)
                        sys.exit(1)
                    nome = "mini_" + str(cont) + ".jpg"
                    cont = cont + 1
                elif sistema == "Windows":
                    cmd = 'python exif.py "' + elemento + '\\' + arquivo + '"'
                    texto = subprocess.check_output(cmd)
                    nome = "mini_" + str(cont) + ".jpg"
                    cont = cont + 1
                else:
                    print "Sistema nao suportado"
                    sys.exit(1)
                metadados.append(texto)
    escreve(metadados, diretorio)

def escreve(metadados, diretorio):
    doc = OpenDocumentText()

    ## cria o estilo para o titulo do documento
    s = doc.styles
    h1style = Style(name="Heading 1", family="paragraph")
    h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold"}))
    s.addElement(h1style)
    h=H(outlinelevel=1, stylename=h1style, text="Arquivo de Metadados")
    doc.text.addElement(h)
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

    # Style for the photo frame
    photostyle = Style(name="MyMaster-photo", family="presentation")
    doc.styles.addElement(photostyle)

    ## cria a tabela e especifica as colunas
    table = Table()
    table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthshort))
    table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthwide))
    
    for imagem in metadados:
        linhas = imagem.split('\n')
        tr = TableRow()
        table.addElement(tr)
        celula = TableCell()
        tr.addElement(celula)
        
        ##teste de celula
        ##p2 = []
        photoframe = Frame(stylename=photostyle, width="128pt", height="128pt", x="336pt", y="56pt")
        ##p2.append(P(stylename=tablecontents,text="teste"))
        celula.addElement(photoframe)
        caminho = linhas[0]
        href = doc.addPicture(caminho[:-2])
        print caminho[:-2]
        photoframe.addElement(Image(href=href))
        
        tc = TableCell()
        tr.addElement(tc)
        p = []
        num = 0
        for linha in linhas:
            p.append(P(stylename=tablecontents,text=""))
            p[num].addText(linha)
            tc.addElement(p[num])
            num = num + 1
    doc.text.addElement(table)
    doc.save("testepython.odt")
    print "Metadados gravados com sucesso no arquivo testepython.odt"

def main():
    extrai(sys.argv[1])

if __name__ == '__main__':
    main()
