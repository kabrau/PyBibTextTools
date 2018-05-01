


            if (pesquisa['lib']=="IEEE") and (not 'abstract' in entry.fields.keys() ):
                site = "https://ieeexplore.ieee.org/document/"+key+"/"
                with urllib.request.urlopen(site) as response:
                    html = response.read()
                    texto = html.decode("utf-8")
                    inicio = texto.find('"abstract":')
                    subtexto = texto[inicio:]
                    abstractSplit = subtexto.split('"')
                    if len(abstractSplit)>=3:
                        entry.fields['abstract'] = abstractSplit[3]
                        print("foi IEEE")




            if (pesquisa['lib']=="ACM") and (not 'abstract' in entry.fields.keys() ) and ('acmid' in entry.fields.keys() ):
                site = "https://dl.acm.org/tab_abstract.cfm?id="+entry.fields['acmid']
                print(site)
                try:
                    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urlopen(req).read()
                    texto = html.decode("utf-8")
                    inicio = texto.find("<p>")+3
                    final = texto.find("</p>")
                    if (inicio > 1 and final > 1):
                        inicio = inicio + 3
                        entry.fields['abstract'] = texto[inicio:final]
                        print("foi ACM")

                finally:
                    pass
                