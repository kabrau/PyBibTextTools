import os
import sys

sys.path.insert(0, './pybtex/')
from pybtex.database import parse_file
from pybtex.database import BibliographyData, Entry

import unidecode
import urllib.request
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import re
import argparse


#=============================================================
def run(database, bibFileName, proxy, limit):

    print("=========================================")
    print("DATABASE ", database, limit)
    print("=========================================")

    if not os.path.isfile(bibFileName):
        print("File not found: ",bibFileName)
        return

    bibData = parse_file(bibFileName)

    processed = 0
    urlError = 0
    hadAbstract = 0
    getAbstract = 0
    withoutAcmId = 0

    for entry in bibData.entries.values():
        processed = processed + 1
        
        print(processed, entry.key+": ", end="", flush=True)

        if "abstract" in entry.fields.keys():
            hadAbstract = hadAbstract + 1
            print("had abstract")

        elif database=="acm" and not 'acmid' in entry.fields.keys():
            withoutAcmId = withoutAcmId + 1

        else:

            if database=="springer":
                site = entry.fields['url']
                if site.find("chapter") != -1:
                    site = "http://link.springer.com/chapter/"
                else:
                    site = "http://link.springer.com/article/"
                
                site = site+entry.key
            
            elif database=="acm":
                site = "https://dl.acm.org/tab_abstract.cfm?id="+entry.fields['acmid']

            elif database=="ieee":
                site = "https://ieeexplore.ieee.org/document/"+entry.key+"/"
                
            
            try:
                if not proxy==None: 
                    #use Proxy
                    proxy_handler=urllib.request.ProxyHandler({"https":proxy})
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)

                req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
                html = urlopen(req).read()
                htmlText = html.decode("utf-8")

                if database=="springer":
                    inicio = htmlText.find('<strong class="EmphasisTypeBold ">Abstract.</strong>')
                    if inicio == -1:
                        inicio = htmlText.find('<h2 class="Heading">Abstract</h2>')
                    if inicio == -1:
                        inicio = htmlText.find('<h2 class="Heading">Abstract.</h2>')
                    if inicio == -1:
                        inicio = htmlText.find('Abstract')

                    htmlText = htmlText[inicio:]

                    inicio =  htmlText.find('<p ')
                    if inicio>-1 and inicio<50:
                        htmlText = htmlText[inicio:]

                    final = htmlText.find('</section>')
                    subhtmlText = htmlText[0:final]

                    texto = re.sub("<.*?>", "", subhtmlText)
                
                elif database=="acm":
                    texto = re.sub("<.*?>", "", htmlText)

                elif database=="ieee":
                    inicio = htmlText.find('"abstract":')
                    subtexto = texto[inicio:]
                    abstractSplit = subtexto.split('"')
                    if len(abstractSplit)>=3:
                        texto = abstractSplit[3]

                if texto=="":
                    print("Abstract not found")
                else:
                    print("Loaded")
                    entry.fields['abstract'] = texto

                entry.fields['url'] = site
                if database=="springer":
                    entry.fields['doi'] = entry.key

                bibData.entries[entry.key] = entry
                getAbstract = getAbstract + 1
                
            except:
                print("url error ", sys.exc_info())
                urlError = urlError + 1

            
            if getAbstract >= limit:
                break 


    print("")
    print("Had Abstract ", hadAbstract)
    print("Url errors ", urlError)
    if (withoutAcmId>0):
        print("Without ACM id ", withoutAcmId)

    print("Loaded Abstract", getAbstract)
    print("Total Entries ", len(bibData.entries))
    print("Limit to process ", limit)
    print("Processed ", processed)
    if (processed<len(bibData.entries)):
        print("Left ", len(bibData.entries) - processed)


    bibData.to_file(bibFileName)


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--database", choices=['springer', 'acm', 'ieee'], required=True, help="select database")
ap.add_argument("-f", "--bibFileName", required=True, help="Springer bibFile name")

ap.add_argument("-p", "--proxy", required=False, help="internet proxy, ex: https://john:password123@palmas.pucrs.br:4001")

ap.add_argument("-l", "--limit", required=False, help="abstract load limit", default=9999, type=int)

args = vars(ap.parse_args())

run(args["database"], args["bibFileName"], args["proxy"], args["limit"])




    


