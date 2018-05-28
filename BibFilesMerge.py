import os
import sys

sys.path.insert(0, './pybtex/')
from pybtex.database import parse_file
from pybtex.database import BibliographyData, Entry

import unidecode
import argparse

mergedCont = 0 

#=============================================================
def mergeEntry(original, novo):
    global mergedCont
    merged = False

    yearOut = int(original.fields['year'])
    year2 = int(novo.fields['year'])
    if (year2>yearOut):
        original.fields['year'] = novo.fields['year']
        merged = True

    for novoKey in novo.fields.keys():
        if novoKey not in original.fields.keys():
            original.fields[novoKey] = novo.fields[novoKey]
            merged = True

    abs1 = ""
    abs2 = ""
    if "abstract" in original.fields.keys():
        abs1 = original.fields['abstract']
    if "abstract" in novo.fields.keys():
        abs2 = novo.fields['abstract']
    if (len(abs2)>len(abs1)):
        original.fields['abstract'] = novo.fields['abstract']
        original.fields['source'] = original.fields['source'] +";" + novo.fields['source']
        merged = True

    if merged:
        mergedCont = mergedCont + 1

    return original


#=============================================================
def run(folderPath, fileList, fileNameOut):
    global mergedCont

    fileNamePathOut = os.path.join(folderPath, fileNameOut)

    bibDataOut = BibliographyData()

    total = 0
    mergedCont = 0 
    withoutAuthor = 0
    withoutYear = 0 
    withoutJornal = 0
    duplicates = 0

    for bibFileName in fileList:
        print(bibFileName,"                                             ")    

        bibData = parse_file(os.path.join(folderPath,bibFileName))

        for entry in bibData.entries.values():
            total = total + 1

            if not 'author' in entry.persons.keys():
                withoutAuthor = withoutAuthor + 1
            elif not 'year' in entry.fields.keys() or int(entry.fields['year'])==0:
                withoutYear = withoutYear + 1
            elif (not 'journal' in entry.fields.keys() ) and (not 'booktitle' in entry.fields.keys() ):
                withoutJornal = withoutJornal + 1
            else:                
                key =  entry.key.lower()
                print("Key "+key+"               \r", end="", flush=True)

                entry.fields['source'] = bibFileName
                oldEntry = None

                for entryOut in bibDataOut.entries.values():
                    if (entryOut.fields['title'].lower()==entry.fields['title'].lower()):
                        year = int(entry.fields['year'])
                        yearOut = int(entryOut.fields['year'])
                        diff = abs(year-yearOut)
                        if (diff==0):
                            oldEntry = entryOut
                        elif (diff==1 or diff==2):
                            try:
                                lastname = unidecode.unidecode(entry.persons['author'][0].last_names[0]).lower()
                            except :
                                lastname = ""
                                
                            try:
                                lastNameOut = unidecode.unidecode(entryOut.persons['author'][0].last_names[0]).lower()
                            except :
                                lastNameOut = ""
                                
                            try:
                                firstName = unidecode.unidecode(entry.persons['author'][0].firstNames[0]).lower()
                            except :
                                firstName = ""
                                
                            try:
                                firstNameOut = unidecode.unidecode(entryOut.persons['author'][0].firstNames[0]).lower()
                            except :
                                firstNameOut = ""

                            if (lastname==lastNameOut or lastname==firstNameOut or lastNameOut==firstName):
                                oldEntry = entryOut


  
                if (oldEntry != None):
                    duplicates = duplicates + 1
                    bibDataOut.entries[oldEntry.key] = mergeEntry(oldEntry, entry)

                else:
                    while (key in bibDataOut.entries.keys()):
                        key = key +"_a"
                    bibDataOut.entries[key] = entry

    print("                                                     ")
    print("Total ", total)

    print("without Author ", withoutAuthor)
    print("without Year ", withoutYear)
    print("without Jornal or conference or booktitle", withoutJornal)

    print("Duplicates ", duplicates, " merged ",mergedCont)
    print("Final ", len(bibDataOut.entries))

    withoutAbstract = 0 
    for entry in bibDataOut.entries.values():
        if not 'abstract' in entry.fields.keys():
            withoutAbstract = withoutAbstract + 1
        

    print("without Abstract ", withoutAbstract)

    bibDataOut.to_file(fileNamePathOut)



#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--folderPath", required=True, help="Bib files folder path")
ap.add_argument("-f", "--fileList", nargs='*', required=False, help='bib file name list, e.g. -files IEEE.bib ACM.bib science.bib Springer.bib')
ap.add_argument("-o", "--fileNameOut", required=False, help="File name of merged file")

args = vars(ap.parse_args())

print("-p ",args["folderPath"])
print("-o ",args["fileNameOut"])
print("-f ",args["fileList"])

run(args["folderPath"], args["fileList"], args["fileNameOut"])

#python BibFilesMerge.py -p "E:\Google Drive\Doutorado\Revisão Sistematica\resultados pesquisas" -o "MyFile.bib" -f IEEE.bib ACM.bib science.bib Springer.bib
    
#python BibFilesMerge.py -p "E:\Google Drive\Doutorado\Revisão Sistematica\resultados pesquisas" -f IEEE.bib ACM.bib science.bib Springer.bib -o "MyFile.bib" 

