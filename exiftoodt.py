#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

## verifica a presenca ou nao da PIL instalada
try:
    from PIL import Image
    PIL_ok = True
except:
    PIL_ok = False
    print "PIL nao detectada. Instale a Python Imaging Library"
    sys.exit(1)
    
if PIL_ok:
    ## importa as bibliotecas que serao usadas no programa
    import sys,os,platform,commands,subprocess
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties, MasterPage, \
    TableColumnProperties, PageLayout, PageLayoutProperties, GraphicProperties, DrawingPageProperties
    from odf.text import H, P, Span
    from odf.table import Table, TableColumn, TableRow, TableCell
    from miniatura import mini

def busca(diretorio):
    ## cria listas para armazenar conteudo, alem de iniciar variaveis,
    ## incluindo a que define as extensoes de imagem
    pastas = []
    sistema = platform.system() ## detecta o sistema em uso
    extensions = ['.jpeg', '.jpg', '.jpe', '.tga', '.gif', '.tif', '.bmp', '.rle', '.pcx', '.png', '.mac', '.pnt', '.pntg', '.pct', '.pic', '.pict', '.qti', '.qtif']
    
    ## tenta criar o diretorio 'mini' para armazenar as miniatura
    ## o comando so eh executado caso a pasta nao exista
    try:
        os.mkdir ('mini')
    except:
        pass
    
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
                    mini(elemento + '/', arquivo) ## chama a funcao para criar a miniatura
                    extrailin(elemento, arquivo) ## chama a funcao para extrair os metadados
                elif sistema == "Windows":
                    mini(elemento + '\\', arquivo)
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
    linhas = texto.split('\n') ## separa cada linha de texto dos metadados
    ## cria uma linha da tabela
    tr = TableRow()
    table.addElement(tr)
    ## cria a primeira coluna onde deve ficar a miniatura
    celula = TableCell()
    tr.addElement(celula)
    ## cria a segunda coluna onde ficam os metadados em si
    tc = TableCell()
    tr.addElement(tc)
    ## adiciona linha a linha os metadados
    for linha in linhas:
        tc.addElement(P(stylename=tablecontents,text=linha))

def main():
    nome = 'arquivo de metadados' ## nome do arquivo
    try:
        caminho = sys.argv[1]
    except:
        caminho = raw_input("Insira o caminho da pasta a ser processada: ")
    busca(caminho)
    
    doc.text.addElement(table)
    doc.save(nome,True)
    print "Metadados gravados com sucesso no arquivo \"" + nome + ".odt\""

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
