import urllib.request
from html.parser import HTMLParser
from urllib.request import Request, urlopen

site = "https://dl.acm.org/tab_abstract.cfm?id=2876722"

req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})

html = urlopen(req).read()

texto = html.decode("utf-8")

inicio = texto.find("<p>")+3
final = texto.find("</p>")

subtexto = texto[inicio:final]

print( subtexto )


