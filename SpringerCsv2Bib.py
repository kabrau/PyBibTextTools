import os
import sys

sys.path.insert(0, './pybtex/')
from pybtex.database import parse_file, parse_string
from pybtex.database import BibliographyData, Entry, Person

import io
import csv
import pandas as pd
import argparse
import unidecode
from shutil import copyfile
import tempfile

#=============================================================
def TypePaperSelect(type_tmp):
    typePaper = 'InProceedings'
    if (type_tmp=='Article'):
        typePaper = 'article'
    elif (type_tmp=='Chapter'):
        typePaper = 'InProceedings'
    return type_tmp

#=============================================================
def AuthorFix(author_tmp):

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

    return author

#=============================================================
def run(csvFileName, bibFileName):

    if not os.path.isfile(csvFileName):
        print("File not found: ",csvFileName)
        return

    # I dont kown Why, but dont work complex path in Panda, then I copy file to local path
    tmpFile = tempfile.mktemp()
    copyfile(csvFileName,tmpFile)

    colnames = ['title','journal','book','volume','issue','doi','author','year','url','type']
    pn = pd.read_csv(tmpFile, names=colnames, skiprows=1) 


    bibData = BibliographyData()
    total = 0
    notAuthor = 0

    for row_index, row in pn.iterrows():
        total = total + 1
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
            fields.append(('author', AuthorFix(row.author)))

        keyPaper = row.doi
        typePaper = TypePaperSelect(row.type)

        print("Chave "+keyPaper+"               \r", end="", flush=True)

        if (pd.isnull(row.author)):
            notAuthor = notAuthor + 1
        else:
            bibData.entries[keyPaper] = Entry(typePaper, fields)

    print("Processed ",total,"                             ")
    print("Removed without author ", notAuthor)
    print("Total Final",len(bibData.entries))

    bibData.to_file(bibFileName)
    print("Saved file ",bibFileName)

#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--csvFileName", required=True, help="CSV file name")
ap.add_argument("-b", "--bibFileName", required=True, help="BibText file name")

args = vars(ap.parse_args())

run(args["csvFileName"], args["bibFileName"])