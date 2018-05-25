import csv
import pandas as pd

from pybtex.database import parse_file, parse_string
from pybtex.database import BibliographyData, Entry, Person

import unidecode

#fileName = "E:/Google Drive/Doutorado/Revisão Sistematica/resultados pesquisas/Springer.csv"

fileName = "Springer.csv"
bibFileName = "Springer.bib" #os.path.join(folder,"Springer.bib")

bigFinal = BibliographyData()

colnames = ['title','journal','book','volume','issue','doi','author','year','url','type']
pn = pd.read_csv(fileName, names=colnames, skiprows=1) 

print("===========================================================")
print("CSV Reading")

for row_index,row in pn.iterrows():
   fields = []
   if (not pd.isnull(row.title)):
        fields.append(('title', row.title))
   if (not pd.isnull(row.journal)):
        fields.append(('journal', row.journal))
   if (not pd.isnull(row.volume)):
        fields.append(('volume', str(row.volume)))
   if (not pd.isnull(row.volume)):
        fields.append(('issue', str(row.issue)))
   if (not pd.isnull(row.doi)):
        fields.append(('doi', row.doi))
   if (not pd.isnull(row.year)):
        fields.append(('year', str(row.year)))
   if (not pd.isnull(row.url)):
        fields.append(('url', row.url))

   if (not pd.isnull(row.author)):
        author_tmp = row.author

        #problems with spring CSV
        
        # "Sergey Ablameyko PhD, DSc, Prof, FIEE, FIAPR, SMIEEETony Pridmore BSc, PhD"
        # correct is
        # "Sergey Ablameyko and Tony Pridmore"
        author_tmp = author_tmp.replace(","," ")
        author_tmp = author_tmp.replace("PhD","")
        author_tmp = author_tmp.replace("DSc","")
        author_tmp = author_tmp.replace("Prof","")
        author_tmp = author_tmp.replace("FIEE","")
        author_tmp = author_tmp.replace("FIAPR","")
        author_tmp = author_tmp.replace("SMIEEE","")
        author_tmp = author_tmp.replace("  "," ")

        # "Yingying ZhuCong YaoXiang Bai"
        # correct is
        # "Yingying Zhu and Cong Yao and Xiang Bai"
        last_word_isalpha = False
        author = ""
        for word in author_tmp:
            is_uppercase = word.isupper() and word.isalpha()
            if (is_uppercase and last_word_isalpha):
                author = author + " and "
            author = author + word
            last_word_isalpha = word.islower() and word.isalpha()

        fields.append(('author', author))


   keyPaper = row.doi
   
   typePaper = 'InProceedings'
   if (row.type=='Article'):
        typePaper = 'article'
   elif (row.type=='Chapter'):
        typePaper = 'InProceedings'

   if (not pd.isnull(row.author)):
        paper = Entry(typePaper, fields)
        entry = BibliographyData({
            keyPaper: paper
        })
        
        print(row_index,"=>",entry.to_string('bibtex'))
        bigFinal.entries[keyPaper] = Entry(typePaper, fields)
        #print(row_index,"=>",bigFinal)

print("===========================================================")
print("BIB Show")

print("Final ", len(bigFinal.entries))
#for key, entry in bigFinal.entries.iteritems():
#    print(key, entry)

print("===========================================================")
print("BIB Save")

bigFinal.to_file(bibFileName)
print("Saved file ",bibFileName)
