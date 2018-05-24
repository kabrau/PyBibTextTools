import os
import sys
sys.path.insert(0, 'E:/GitHub/pybtex/')

from pybtex.database import parse_file
from pybtex.database import BibliographyData, Entry
import unidecode
import urllib.request
from html.parser import HTMLParser
from urllib.request import Request, urlopen

# NOTE
folder = 'C:/Users/marcelo/Google Drive/Doutorado/Revisão Sistematica/resultados pesquisas/'

# PC
folder = 'E:/Google Drive/Doutorado/Revisão Sistematica/resultados pesquisas/'

origem = os.path.join(folder,"IEEE.bib")
bib_data = parse_file(origem)

destino = os.path.join(folder,"MyIEEE.bib")
bigFinal = BibliographyData()

i = 0
problems = 0
adicionados = 0
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
        else:
            site = "https://ieeexplore.ieee.org/document/"+entry.key+"/"
            with urllib.request.urlopen(site) as response:
                html = response.read()
                texto = html.decode("utf-8")
                inicio = texto.find('"abstract":')
                subtexto = texto[inicio:]
                abstractSplit = subtexto.split('"')
                if len(abstractSplit)>=3:
                    entry.fields['abstract'] = abstractSplit[3]
                    adicionados = adicionados + 1

        bigFinal.entries[entry.key] = entry



print("")
print("Total ", i)
print("Problemas ", problems)
print("Tem Abstract ", comAbs)
print("Adicionados Abstract", adicionados)

bigFinal.to_file(destino)




    


