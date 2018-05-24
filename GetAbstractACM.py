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

origem = os.path.join(folder,"ACM.bib")
bib_data = parse_file(origem)

destino = os.path.join(folder,"MyACM.bib")
bigFinal = BibliographyData()

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
    elif (not 'journal' in entry.fields.keys() ) and (not 'booktitle' in entry.fields.keys() ):
        problems = problems + 1
    
    else:
        if "abstract" in entry.fields.keys():
            comAbs = comAbs + 1
        elif not 'acmid' in entry.fields.keys():
            semId = semId + 1
        else:
            proxy_handler=urllib.request.ProxyHandler({"https": "https://"+usuario+":"+senha+"@palmas.pucrs.br:4001"})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)

            site = "https://dl.acm.org/tab_abstract.cfm?id="+entry.fields['acmid']
            print(adicionados, site)
            
            req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            texto = html.decode("utf-8")
            texto = re.sub("<.*?>", "", texto)
            entry.fields['abstract'] = texto
            adicionados = adicionados + 1


        bigFinal.entries[entry.key] = entry
        if adicionados > 10:
            break 



print("")
print("Total ", i)
print("Problemas ", problems)
print("Tem Abstract ", comAbs)
print("Sem ID ", semId)
print("Adicionados Abstract", adicionados)

bigFinal.to_file(destino)







    


