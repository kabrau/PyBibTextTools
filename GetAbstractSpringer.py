import os
import sys
sys.path.insert(0, 'E:/GitHub/pybtex/')

from pybtex.database import parse_file
from pybtex.database import BibliographyData, Entry
import unidecode
import urllib.request
from html.parser import HTMLParser
from urllib.request import Request, urlopen

import re

usuario = "17190654"
senha = "xxx"

# NOTE
folder = 'C:/Users/marcelo/Google Drive/Doutorado/Revisão Sistematica/resultados pesquisas/'

# PC
folder = 'E:/Google Drive/Doutorado/Revisão Sistematica/resultados pesquisas/'

origem = os.path.join(folder,"Springer.bib")
bib_data = parse_file(origem)

destino = os.path.join(folder,"Springer.bib")
bigFinal = bib_data 
#bigFinal = BibliographyData()

i = 0
problems = 0
adicionados = 0
semId = 0
comAbs = 0
for entry in bib_data.entries.values():
    i = i + 1

    if not 'author' in entry.persons.keys():
        problems = problems + 1
    elif not 'year' in entry.fields.keys() or int(entry.fields['year'])==0:
        problems = problems + 1
    elif not 'title' in entry.fields.keys() or entry.fields['title']=="Preface":
        problems = problems + 1
    elif (not 'journal' in entry.fields.keys() ) and (not 'booktitle' in entry.fields.keys() ):
        problems = problems + 1
    
    else:
        if "abstract" in entry.fields.keys():
            comAbs = comAbs + 1
        else:
            #proxy_handler=urllib.request.ProxyHandler({"https": "https://"+usuario+":"+senha+"@palmas.pucrs.br:4001"})
            #opener = urllib.request.build_opener(proxy_handler)
            #urllib.request.install_opener(opener)

            site = entry.fields['url']
            if site.find("chapter") != -1:
                site = "http://link.springer.com/chapter/"
            else:
                site = "http://link.springer.com/article/"
            
            site = site+entry.key
            print(adicionados, site)
            
            try:
                req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
                html = urlopen(req).read()
                texto = html.decode("utf-8")

                inicio = texto.find('<strong class="EmphasisTypeBold ">Abstract.</strong>')
                if inicio == -1:
                    inicio = texto.find('<h2 class="Heading">Abstract</h2>')
                if inicio == -1:
                    inicio = texto.find('<h2 class="Heading">Abstract.</h2>')
                if inicio == -1:
                    inicio = texto.find('Abstract')

                texto = texto[inicio:]

                inicio =  texto.find('<p ')
                if inicio>-1 and inicio<50:
                    texto = texto[inicio:]

                final = texto.find('</section>')
                subtexto = texto[0:final]

                subtexto = re.sub("<.*?>", "", subtexto)

                if subtexto=="":
                    print("Abs not found")

                entry.fields['abstract'] = subtexto
                entry.fields['url'] = site
                entry.fields['doi'] = entry.key

                adicionados = adicionados + 1
                
            except:
                print("url error")

            #print(subtexto)

        bigFinal.entries[entry.key] = entry
        if adicionados > 1000:
            break 



print("")
print("Total ", i)
print("Problemas ", problems)
print("Tem Abstract ", comAbs)
print("Adicionados Abstract", adicionados)

bigFinal.to_file(destino)







    


